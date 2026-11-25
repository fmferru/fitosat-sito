import bpy, bmesh, math, random, sys
from mathutils import Vector
args = sys.argv[sys.argv.index('--') + 1:]
RX, RY, SAMPLES, OUT, MODE, Q = int(args[0]), int(args[1]), int(args[2]), args[3], args[4], int(args[5])
random.seed(3)
import time; T0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
RS, NROWS, LEN, DEPTH = 2.5, 13, 70.0, 80.0
XS = [(-(NROWS - 1) / 2 + k) * RS for k in range(NROWS)]

def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes, m.node_tree.links
def node(N, t, **kw):
    n = N.new(t)
    for k, v in kw.items(): n.inputs[k].default_value = v
    return n

# ---------- materiali ----------
def leaf_mat():
    m, N, L = mat('leaf'); b = N['Principled BSDF']
    oi = N.new('ShaderNodeObjectInfo'); pi = N.new('ShaderNodeParticleInfo')
    ramp = N.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].color = (.025, .075, .012, 1); cr.elements[1].color = (.09, .19, .03, 1)
    e = cr.elements.new(.55); e.color = (.05, .13, .02, 1)
    r = N.new('ShaderNodeMath'); r.operation = 'FRACT'
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 7.31
    L.new(pi.outputs['Index'], mul.inputs[0]); L.new(mul.outputs[0], r.inputs[0]); L.new(r.outputs[0], ramp.inputs[0])
    L.new(ramp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = .65
    b.inputs['Specular IOR Level'].default_value = .12
    b.inputs['Transmission Weight'].default_value = 0.0
    b.inputs['Subsurface Weight'].default_value = .15; b.inputs['Subsurface Radius'].default_value = (.1, .2, .05)
    tr = N.new('ShaderNodeBsdfTranslucent'); L.new(ramp.outputs[0], tr.inputs[0])
    mx = N.new('ShaderNodeMixShader'); mx.inputs[0].default_value = .25
    out = N['Material Output']
    L.new(b.outputs[0], mx.inputs[1]); L.new(tr.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs[0])
    return m
def tex_mat(name, c0, c1, scale, rough=.95, bump=.6, coord='Object', detail=8):
    m, N, L = mat(name); b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    nz = node(N, 'ShaderNodeTexNoise', Scale=scale, Detail=detail, Roughness=.6)
    L.new(tc.outputs[coord], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (*c0, 1); ramp.color_ramp.elements[1].color = (*c1, 1)
    L.new(nz.outputs['Fac'], ramp.inputs[0]); L.new(ramp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    fn = node(N, 'ShaderNodeTexNoise', Scale=scale * 12, Detail=10)
    L.new(tc.outputs[coord], fn.inputs['Vector'])
    bp = node(N, 'ShaderNodeBump', Strength=bump); L.new(fn.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    return m
def soil_face_mat():
    m, N, L = mat('profile'); b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    nz = node(N, 'ShaderNodeTexNoise', Scale=.7, Detail=6); L.new(tc.outputs['Object'], nz.inputs['Vector'])
    add = N.new('ShaderNodeMath'); add.operation = 'MULTIPLY_ADD'; add.inputs[1].default_value = .55
    L.new(nz.outputs['Fac'], add.inputs[0]); L.new(sep.outputs['Z'], add.inputs[2])
    mr = node(N, 'ShaderNodeMapRange'); mr.inputs[1].default_value = -12.0; mr.inputs[2].default_value = .55
    L.new(add.outputs[0], mr.inputs[0])
    ramp = N.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    st = [(0, (.07, .055, .042)), (.3, (.085, .058, .036)), (.5, (.06, .037, .022)), (.68, (.035, .022, .013)), (.82, (.018, .012, .008)), (.93, (.012, .009, .006))]
    cr.elements[0].position, cr.elements[0].color = st[0][0], (*st[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = st[1][0], (*st[1][1], 1)
    for p, c in st[2:]:
        e = cr.elements.new(p); e.color = (*c, 1)
    L.new(mr.outputs[0], ramp.inputs[0])
    # macchie di ossidazione e sassolini
    vo = node(N, 'ShaderNodeTexVoronoi', Scale=9); L.new(tc.outputs['Object'], vo.inputs['Vector'])
    sp = node(N, 'ShaderNodeMapRange'); sp.inputs[1].default_value = .05; sp.inputs[2].default_value = .12; sp.inputs[3].default_value = 1; sp.inputs[4].default_value = 0
    L.new(vo.outputs['Distance'], sp.inputs[0])
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[7].default_value = (.13, .11, .09, 1)
    L.new(sp.outputs[0], mix.inputs['Factor']); L.new(ramp.outputs[0], mix.inputs[6])
    vn = node(N, 'ShaderNodeTexNoise', Scale=6, Detail=10, Roughness=.7); L.new(tc.outputs['Object'], vn.inputs['Vector'])
    vr = node(N, 'ShaderNodeMapRange'); vr.inputs[3].default_value = .6; vr.inputs[4].default_value = 1.45
    L.new(vn.outputs['Fac'], vr.inputs[0])
    vc = N.new('ShaderNodeCombineColor')
    for k in range(3): L.new(vr.outputs[0], vc.inputs[k])
    m2 = N.new('ShaderNodeMix'); m2.data_type = 'RGBA'; m2.blend_type = 'MULTIPLY'; m2.inputs['Factor'].default_value = 1
    L.new(mix.outputs[2], m2.inputs[6]); L.new(vc.outputs[0], m2.inputs[7])
    L.new(m2.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = .98
    fn = node(N, 'ShaderNodeTexNoise', Scale=40, Detail=12); L.new(tc.outputs['Object'], fn.inputs['Vector'])
    h = N.new('ShaderNodeMath'); h.operation = 'ADD'; L.new(fn.outputs['Fac'], h.inputs[0]); L.new(sp.outputs[0], h.inputs[1])
    bp = node(N, 'ShaderNodeBump', Strength=1.0, Distance=.05); L.new(h.outputs[0], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    return m
def simple(name, col, rough=.7, metal=0.):
    m, N, L = mat(name); b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m

LEAF = leaf_mat()
GRASS = tex_mat('grass', (.02, .04, .01), (.05, .08, .02), .6, bump=.4)
DIRT = tex_mat('dirt', (.12, .08, .05), (.22, .15, .09), 1.5, bump=1.0)
PROFILE = soil_face_mat()
BARK = tex_mat('bark', (.05, .035, .025), (.13, .09, .06), 8, rough=.9, bump=1.2)
ROOT = tex_mat('root', (.10, .07, .045), (.2, .14, .09), 12, rough=.75, bump=.8)
POST = tex_mat('post', (.08, .06, .045), (.16, .12, .085), 3, rough=.85)
WIRE = simple('wire', (.6, .6, .6), .35, 1.0)
STONE = tex_mat('stone', (.12, .11, .095), (.26, .24, .2), 4, rough=.8, bump=1.5)
GRASSH = simple('grasshair', (.035, .07, .018), .7)

def link(o):
    sc.collection.objects.link(o); return o
_P = {}
def proto(kind, m):
    key = (kind, m.name)
    if key not in _P:
        if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=10)
        elif kind == 'ico': bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
        p = bpy.context.object; p.data.materials.append(m); p.hide_render = True; p.location = (0, 0, -100); _P[key] = p.data
    return _P[key]
def inst(kind, m, loc, scale, rot=(0, 0, 0)):
    o = bpy.data.objects.new(kind, proto(kind, m)); sc.collection.objects.link(o)
    o.location = loc; o.scale = scale; o.rotation_euler = rot; return o
def mesh_obj(name, verts, faces, m):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); o.data.materials.append(m); return link(o)

# ---------- terreno: superficie e sezione ----------
W = (NROWS + 1) * RS
bpy.ops.mesh.primitive_plane_add(size=1); top = bpy.context.object
top.scale = (W, LEN, 1); top.location = (0, LEN / 2, 0); top.data.materials.append(GRASS)
bpy.ops.object.transform_apply(scale=True)
# fascia di terra sotto i filari
for x in XS:
    bpy.ops.mesh.primitive_plane_add(size=1); s = bpy.context.object
    s.scale = (.9, LEN, 1); s.location = (x, LEN / 2, .004); s.data.materials.append(DIRT)
# erba (peli) nell'interfila
ps = top.modifiers.new('grass', 'PARTICLE_SYSTEM').particle_system
st = ps.settings; st.type = 'HAIR'; st.count = 110000 if Q else 20000; st.hair_length = .13
st.use_advanced_hair = True; st.use_rotations = True; st.rotation_factor_random = .3
st.child_type = 'INTERPOLATED'; st.rendered_child_count = 3; st.child_radius = .08; st.render_type = 'PATH'
top.data.materials.append(GRASSH); st.material = 2
# sezione verticale (faccia verso la camera, y = 0)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=520, y_subdivisions=160, size=1)
face = bpy.context.object; face.rotation_euler = (math.radians(90), 0, 0)
face.scale = (120, DEPTH, 1); face.location = (0, 0, -DEPTH / 2)
bpy.ops.object.transform_apply(rotation=True, scale=True)
t = bpy.data.textures.new('clods', 'CLOUDS'); t.noise_scale = .08; t.noise_depth = 4
dm = face.modifiers.new('d', 'DISPLACE'); dm.texture = t; dm.strength = .06; dm.direction = 'Y'; dm.texture_coords = 'GLOBAL'
face.data.materials.append(PROFILE); face.pass_index = 1
# sassi semi-affioranti
for _ in range(300):
    d = random.uniform(.5, 9.0); r = random.uniform(.012, .05) * (1 + d / 2)
    inst('ico', STONE, (random.uniform(-W / 2, W / 2), random.uniform(.0, .02) + r * .5, -d), (r * random.uniform(.7, 1.4), r, r * random.uniform(.6, 1)), [random.random() * 6 for _ in range(3)])

# ---------- radici (sulla sezione) ----------
def tube(points, radii, m):
    cu = bpy.data.curves.new('root', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 1; cu.bevel_resolution = 3
    sp = cu.splines.new('NURBS'); sp.points.add(len(points) - 1)
    for p, (co, r) in enumerate(zip(points, radii)):
        sp.points[p].co = (*co, 1); sp.points[p].radius = r
    sp.use_endpoint_u = True; sp.order_u = 3
    o = bpy.data.objects.new('root', cu); o.data.materials.append(m); link(o); o.pass_index = 1
def grow(x, z, dx, dz, r, depth=0):
    pts, rad = [], []
    for i in range(22):
        pts.append((x, random.uniform(-.015, .02), z)); rad.append(r)
        ang = math.atan2(dz, dx) + random.gauss(0, .35)
        step = .16 + random.random() * .1
        dx, dz = math.cos(ang), math.sin(ang)
        if dz > -.15: dz -= .25
        x += dx * step; z += dz * step; r *= .9
        if z < -DEPTH + .05 or r < .003: break
        if depth < 3 and random.random() < .26:
            s = random.choice((-1, 1)); grow(x, z, s * 1.0, -.4, r * .65, depth + 1)
    if len(pts) > 2: tube(pts, rad, ROOT)
for x in XS:
    for k in range(3):
        grow(x + random.uniform(-.1, .1), -.05, random.uniform(-.5, .5), -1, random.uniform(.035, .055))

# ---------- viti ----------
bpy.ops.mesh.primitive_plane_add(size=1); leafp = bpy.context.object; leafp.name = 'leafproto'
bm = bmesh.new(); bm.from_mesh(leafp.data); bm.clear()
pts = []
for i in range(26):
    a = i / 26 * 2 * math.pi
    rr = .5 + .18 * math.cos(5 * a) + .08 * math.cos(10 * a)
    pts.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr * .95 + .1, 0)))
bm.faces.new(pts); bm.to_mesh(leafp.data); bm.free()
leafp.data.materials.append(LEAF); leafp.location = (0, 400, -50)
def hedge(x, y0, y1):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co = Vector((x + v.co.x * .55, (y0 + y1) / 2 + v.co.y * (y1 - y0), 1.35 + v.co.z * 1.0))
    long_e = [e for e in bm.edges if abs(e.verts[0].co.y - e.verts[1].co.y) > 1]
    bmesh.ops.subdivide_edges(bm, edges=long_e, cuts=int((y1 - y0) / .4), use_grid_fill=True)
    me = bpy.data.meshes.new('hedge'); bm.to_mesh(me); bm.free()
    h = bpy.data.objects.new('hedge', me); link(h)
    mm = h.modifiers.new('s', 'SUBSURF'); mm.levels = 2; mm.render_levels = 2
    tx = bpy.data.textures.new('hb', 'CLOUDS'); tx.noise_scale = .35
    dd = h.modifiers.new('d', 'DISPLACE'); dd.texture = tx; dd.strength = .25; dd.texture_coords = 'GLOBAL'
    h.data.materials.append(LEAF)
    p = h.modifiers.new('leaves', 'PARTICLE_SYSTEM').particle_system.settings
    p.type = 'HAIR'; p.use_advanced_hair = True; p.count = int((y1 - y0) * (1000 if Q else 120))
    p.render_type = 'OBJECT'; p.instance_object = leafp; p.particle_size = 2.2; p.size_random = .5
    p.use_rotations = True; p.rotation_mode = 'NOR'; p.phase_factor_random = 2.0; p.rotation_factor_random = .6
    p.hair_length = .1
    h.show_instancer_for_render = True
    return h
for x in XS:
    hedge(x, -.15, LEN)
    for y in [.6 + k for k in range(40)]:
        inst('cyl', BARK, (x + random.uniform(-.04, .04), y, .45), (.045, .045, .9), (random.uniform(-.08, .08), random.uniform(-.08, .08), 0))
    for y in range(0, int(LEN), 6):
        inst('cyl', POST, (x, y + .3, 1.0), (.035, .035, 2.0))
    for z in (.85, 1.25, 1.65):
        inst('cyl', WIRE, (x, LEN / 2 + .3, z), (.006, .006, LEN), (math.radians(90), 0, 0))

# ---------- luce, camera ----------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
sky = w.node_tree.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'
sky.sun_elevation = math.radians(28); sky.sun_rotation = math.radians(60); sky.sun_size = math.radians(1.2); sky.air_density = 1.4; sky.dust_density = 2.5
bg = w.node_tree.nodes['Background']; w.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = .12
al = bpy.data.lights.new('fill', 'AREA'); al.energy = 2500; al.size = 12; al.color = (1, .95, .88)
alo = bpy.data.objects.new('fill', al); link(alo); alo.location = (0, -14, 1.5); alo.rotation_euler = (math.radians(95), 0, 0)
cam = bpy.data.cameras.new('cam'); cam.lens = 30 if MODE == 'l' else 24
co = bpy.data.objects.new('cam', cam); link(co); sc.camera = co
if MODE == 'l':
    co.location = (0, -9.0, 5.0); tgt = Vector((0, -0.43, -0.15))
else:
    co.location = (0, -9.0, 7.0); tgt = Vector((0, -9 + 10 * math.cos(math.radians(46)), 7 - 10 * math.sin(math.radians(46))))
co.rotation_euler = (tgt - co.location).to_track_quat('-Z', 'Y').to_euler()

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.cycles.use_auto_tile = True; sc.cycles.tile_size = 512; sc.cycles.denoising_prefilter = 'FAST'
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -.2
# foschia con il mist pass
vl = bpy.context.view_layer; vl.use_pass_mist = True
w.mist_settings.start = 22; w.mist_settings.depth = 70; w.mist_settings.falloff = 'QUADRATIC'
sc.use_nodes = True; T = sc.node_tree; T.nodes.clear()
rl = T.nodes.new('CompositorNodeRLayers'); mx = T.nodes.new('CompositorNodeMixRGB'); mx.blend_type = 'MIX'
mx.inputs[2].default_value = (.70, .70, .66, 1)
mm = T.nodes.new('CompositorNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = .75
vl.use_pass_object_index = True
idm = T.nodes.new('CompositorNodeIDMask'); idm.index = 1
T.links.new(rl.outputs['IndexOB'], idm.inputs[0])
inv = T.nodes.new('CompositorNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
T.links.new(idm.outputs[0], inv.inputs[1])
mm2 = T.nodes.new('CompositorNodeMath'); mm2.operation = 'MULTIPLY'
T.links.new(rl.outputs['Mist'], mm.inputs[0]); T.links.new(mm.outputs[0], mm2.inputs[0]); T.links.new(inv.outputs[0], mm2.inputs[1])
T.links.new(mm2.outputs[0], mx.inputs[0])
T.links.new(rl.outputs['Image'], mx.inputs[1])
comp = T.nodes.new('CompositorNodeComposite'); T.links.new(mx.outputs[0], comp.inputs[0])
sc.render.filepath = OUT
import time; print('BUILD', time.time() - T0, flush=True)
h0 = [o for o in sc.objects if o.name.startswith('Cube')][:2]
for o in h0: print('HEDGE', o.name, o.location, o.dimensions, o.hide_render, o.show_instancer_for_render, [m.type for m in o.modifiers], flush=True)
t1 = time.time(); bpy.ops.render.render(write_still=True); print('RENDER', time.time() - t1, flush=True)
