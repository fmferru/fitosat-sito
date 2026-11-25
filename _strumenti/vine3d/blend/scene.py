import bpy, bmesh, math, random, json, sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

RES_X, RES_Y, SAMPLES = [int(a) for a in sys.argv[sys.argv.index('--') + 1:][:3]]
OUT = sys.argv[sys.argv.index('--') + 4]
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------------- parametri ----------------
NR, RS = 10, 2.6             # filari, distanza tra filari (m)
L, PS = 30.0, 1.0            # lunghezza filare, distanza piante
MX, MY = 2.2, 2.0            # margini
FX, FY = L + 2 * MX, (NR - 1) * RS + 2 * MY
T = 6.0                      # spessore blocco
VIG_ROW, GAP_ROW = 8, 5
GAPS = {7, 8, 9, 19, 20}
ZONE = (0, 2, 18.5, 28.5)    # righe r0..r1, x0..x1
def row_y(r): return MY + r * RS
def pl_x(i): return MX + (i + .5) * PS

# ---------------- materiali ----------------
def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes, m.node_tree.links

def leaf_mat():
    m, N, Lk = mat('leaf'); b = N['Principled BSDF']
    oi = N.new('ShaderNodeObjectInfo')
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 9; nz.inputs['Detail'].default_value = 6
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 26
    Lk.new(tc.outputs['Object'], vo.inputs['Vector'])
    mr = N.new('ShaderNodeMapRange'); mr.inputs[3].default_value = .55; mr.inputs[4].default_value = 1.25
    Lk.new(nz.outputs['Fac'], mr.inputs[0])
    mul = N.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1
    Lk.new(oi.outputs['Color'], mul.inputs[6])
    comb = N.new('ShaderNodeCombineColor')
    for k in range(3): Lk.new(mr.outputs[0], comb.inputs[k])
    Lk.new(comb.outputs[0], mul.inputs[7])
    Lk.new(mul.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = .72
    b.inputs['Subsurface Weight'].default_value = .08
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .9
    Lk.new(vo.outputs['Distance'], bp.inputs['Height']); Lk.new(bp.outputs[0], b.inputs['Normal'])
    return m

def grass_mat():
    m, N, Lk = mat('grass'); b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = .35; nz.inputs['Detail'].default_value = 8
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.03, .075, .012, 1); ramp.color_ramp.elements[1].color = (.07, .12, .02, 1)
    Lk.new(nz.outputs['Fac'], ramp.inputs[0]); Lk.new(ramp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = .95
    fn = N.new('ShaderNodeTexNoise'); fn.inputs['Scale'].default_value = 60
    Lk.new(tc.outputs['Object'], fn.inputs['Vector'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .5
    Lk.new(fn.outputs['Fac'], bp.inputs['Height']); Lk.new(bp.outputs[0], b.inputs['Normal'])
    return m

def soil_strip_mat():
    m, N, Lk = mat('strip'); b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 8
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.13, .075, .04, 1); ramp.color_ramp.elements[1].color = (.24, .15, .08, 1)
    Lk.new(nz.outputs['Fac'], ramp.inputs[0]); Lk.new(ramp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 1
    return m

def earth_mat():
    m, N, Lk = mat('earth'); b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    sep = N.new('ShaderNodeSeparateXYZ'); Lk.new(tc.outputs['Object'], sep.inputs[0])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = .3; nz.inputs['Detail'].default_value = 5
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    add = N.new('ShaderNodeMath'); add.operation = 'MULTIPLY_ADD'; add.inputs[1].default_value = 1.6
    Lk.new(nz.outputs['Fac'], add.inputs[0]); Lk.new(sep.outputs['Z'], add.inputs[2])
    ramp = N.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    # Z va da -T (fondo) a 0 (sopra); valore = z + 1.4*noise (~ -6..1.4)
    mr = N.new('ShaderNodeMapRange'); mr.inputs[1].default_value = -T / 2 + .3; mr.inputs[2].default_value = T / 2 + 1.25
    Lk.new(add.outputs[0], mr.inputs[0]); Lk.new(mr.outputs[0], ramp.inputs[0])
    stops = [(0.0, (.17, .14, .11)), (.22, (.30, .19, .09)), (.42, (.24, .12, .045)), (.62, (.15, .07, .028)),
             (.80, (.075, .035, .014)), (.89, (.05, .024, .01)), (.93, (.04, .08, .014))]
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*stops[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = stops[1][0], (*stops[1][1], 1)
    for p, c in stops[2:]:
        e = cr.elements.new(p); e.color = (*c, 1)
    # sassi
    vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 2.2
    Lk.new(tc.outputs['Object'], vo.inputs['Vector'])
    st = N.new('ShaderNodeMapRange'); st.inputs[1].default_value = .12; st.inputs[2].default_value = .2
    st.inputs[3].default_value = 1; st.inputs[4].default_value = 0
    Lk.new(vo.outputs['Distance'], st.inputs[0])
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[7].default_value = (.22, .2, .17, 1)
    Lk.new(st.outputs[0], mix.inputs['Factor']); Lk.new(ramp.outputs[0], mix.inputs[6])
    Lk.new(mix.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = .97
    fn = N.new('ShaderNodeTexNoise'); fn.inputs['Scale'].default_value = 5; fn.inputs['Detail'].default_value = 10
    Lk.new(tc.outputs['Object'], fn.inputs['Vector'])
    hb = N.new('ShaderNodeMath'); hb.operation = 'ADD'
    Lk.new(fn.outputs['Fac'], hb.inputs[0]); Lk.new(st.outputs[0], hb.inputs[1])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .8
    Lk.new(hb.outputs[0], bp.inputs['Height']); Lk.new(bp.outputs[0], b.inputs['Normal'])
    return m

def simple(name, col, rough=.6, metal=0):
    m, N, Lk = mat(name); b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m

LEAF, GRASS, STRIP, EARTH = leaf_mat(), grass_mat(), soil_strip_mat(), earth_mat()
WOOD = simple('wood', (.22, .14, .08), .8); TRUNK = simple('trunk', (.12, .07, .04), .9)
GRAPE = simple('grape', (.045, .012, .07), .45); GOLD = simple('gold', (.8, .55, .2), .25, 1)

# ---------------- blocco di terra ----------------
bpy.ops.mesh.primitive_cube_add(size=1)
blk = bpy.context.object; blk.name = 'block'
blk.scale = (FX, FY, T); blk.location = (FX / 2, FY / 2, -T / 2)
bpy.ops.object.transform_apply(scale=True)
me = blk.data; bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=40, use_grid_fill=True)
bm.to_mesh(me); bm.free()
vg = blk.vertex_groups.new(name='bottom')
vg.add([v.index for v in me.vertices if v.co.z < -T / 2 + .01], 1.0, 'REPLACE')
tex = bpy.data.textures.new('rock', 'CLOUDS'); tex.noise_scale = 3.5; tex.noise_depth = 2
dm = blk.modifiers.new('disp', 'DISPLACE'); dm.texture = tex; dm.strength = .7; dm.vertex_group = 'bottom'; dm.direction = 'Z'
blk.data.materials.append(EARTH)
# la faccia superiore usa il materiale erba
blk.data.materials.append(GRASS)
for p in blk.data.polygons:
    if p.normal.z > .9 and p.center.z > -.01: p.material_index = 1

# strisce di terra sotto i filari
for r in range(NR):
    bpy.ops.mesh.primitive_plane_add(size=1)
    s = bpy.context.object; s.scale = (L + .4, .9, 1); s.location = (FX / 2, row_y(r), .005)
    s.data.materials.append(STRIP)

# ---------------- filari ----------------
def seg_color(r, x):
    g = (.03 + random.uniform(-.006, .006), .095 + random.uniform(-.014, .014), .016)
    sx = math.exp(-(((x - 5) / 6) ** 2 + ((r - 1.2) / 1.6) ** 2))
    c = [g[k] * (1 - .9 * sx) + (.30, .26, .035)[k] * .9 * sx for k in range(3)]
    if r == VIG_ROW and 17 < x < 27:
        f = min(1, (x - 17) / 7); w = min(1, (x - 17) / 1.5, (27 - x) / 1.5)
        hot = [(.75, .26, .02)[k] * (1 - f) + (.55, .04, .02)[k] * f for k in range(3)]
        c = [c[k] * (1 - w) + hot[k] * w for k in range(3)]
    return c

_protos = {}
def inst(kind, loc, matobj, **kw):
    if kind not in _protos:
        if kind.startswith('cyl'): bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=10)
        else: bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=10, ring_count=6)
        p = bpy.context.object; p.data.materials.append(matobj); p.hide_render = True; p.hide_viewport = True; _protos[kind] = p
    o = bpy.data.objects.new(kind, _protos[kind].data.copy() if False else _protos[kind].data); coll.objects.link(o)
    o.location = loc; o.scale = kw.get('scale', (1, 1, 1))
    o['m'] = matobj.name
    return o
proto = None
def make_proto():
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object; o.name = 'segproto'
    o.scale = (1.7, .62, 1.45); bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.modifier_add(type='SUBSURF'); o.modifiers[0].levels = 3; o.modifiers[0].render_levels = 3
    bpy.ops.object.modifier_apply(modifier=o.modifiers[0].name)
    t = bpy.data.textures.new('leafy', 'VORONOI'); t.noise_scale = .16
    m = o.modifiers.new('d', 'DISPLACE'); m.texture = t; m.strength = .16; m.texture_coords = 'GLOBAL'
    o.data.materials.append(LEAF)
    return o
coll = bpy.data.collections.new('vines'); sc.collection.children.link(coll)
proto = make_proto()
for r in range(NR):
    y = row_y(r)
    for i in range(int(L / PS)):
        x = pl_x(i)
        if r == GAP_ROW and i in GAPS:
            inst('cyl_t', (x, y, .17), TRUNK, scale=(.07, .07, .35))
            continue
        o = proto.copy(); o.data = proto.data; coll.objects.link(o)
        for m in proto.modifiers: pass
        o.location = (x, y, 1.55 + random.uniform(-.04, .04))
        o.rotation_euler = (0, 0, random.uniform(-.05, .05))
        o.scale = (1, random.uniform(.9, 1.1), random.uniform(.92, 1.08))
        o.color = (*seg_color(r, x), 1)
        inst('cyl_t', (x, y, .45), TRUNK, scale=(.05, .05, .9))
        # grappoli
        if ZONE[0] <= r <= ZONE[1] and ZONE[2] <= x <= ZONE[3]:
            for side in (-1, 1):
                cx, cy, cz = x + random.uniform(-.2, .2), y + side * .38, 1.1
                for k in range(22):
                    a = random.random() * 6.283; rr = random.uniform(0, .16) * (1 - k / 26)
                    inst('sph_g', (cx + math.cos(a) * rr, cy + math.sin(a) * rr * .6, cz - k * .024), GRAPE, scale=(.085,) * 3)
    for x in (MX - .3, FX - MX + .3) + tuple(MX + k * 6 for k in range(1, 5)):
        inst('cyl_w', (x, y, 1.15), WOOD, scale=(.06, .06, 2.3))
proto.hide_render = True; proto.hide_viewport = True

# spilli
PINS = [(VIG_ROW, 22.5), (1, 4.5)]
for r, x in PINS:
    bpy.ops.mesh.primitive_cylinder_add(radius=.04, depth=1.4, location=(x, row_y(r), 2.6)); bpy.context.object.data.materials.append(GOLD)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.28, location=(x, row_y(r), 3.35)); bpy.context.object.data.materials.append(GOLD)

# piano che raccoglie l'ombra
bpy.ops.mesh.primitive_plane_add(size=200, location=(FX / 2, FY / 2, -T - 3.5))
bpy.context.object.is_shadow_catcher = True

# ---------------- luce e camera ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (.85, .84, .82, 1); bg.inputs[1].default_value = .8
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.8; sun.angle = math.radians(8)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
so.rotation_euler = (math.radians(42), 0, math.radians(-25))
cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 58
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
tgt = Vector((FX / 2, FY / 2, -1.6))
co.location = tgt + Vector((-26, -70, 58))
co.rotation_euler = (tgt - co.location).to_track_quat('-Z', 'Y').to_euler()

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = RES_X, RES_Y
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.filepath = OUT
sc.view_settings.exposure = 0
bpy.context.view_layer.update()

def proj(p):
    v = world_to_camera_view(sc, co, Vector(p)); return [v.x * 100, (1 - v.y) * 100]
zx0, zx1 = ZONE[2] - .6, ZONE[3] + .6; zy0, zy1 = row_y(ZONE[0]) - 1.1, row_y(ZONE[1]) + 1.1
an = {'vigoria': proj((19.5, row_y(VIG_ROW), 2.1)), 'fallanze': proj((pl_x(8), row_y(GAP_ROW), .6)),
      'stress': proj((5, row_y(1), 2.2)), 'controlli': proj((22.5, row_y(VIG_ROW), 3.35)),
      'vendemmia': proj((zx1, zy0, 2.3)),
      'zone': [proj((zx0, zy0, 2.3)), proj((zx1, zy0, 2.3)), proj((zx1, zy1, 2.3)), proj((zx0, zy1, 2.3))]}
json.dump(an, open(OUT + '.json', 'w'))
bpy.ops.render.render(write_still=True)
