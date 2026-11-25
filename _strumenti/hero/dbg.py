import bpy
exec(open('hero.py').read().split("# ---------- luce, camera ----------")[0].replace("args = sys.argv[sys.argv.index('--') + 1:]","args = ['10','10','1','x','l','0']"))
dg = bpy.context.evaluated_depsgraph_get()
n = 0; names = {}
for inst in dg.object_instances:
    if inst.is_instance:
        n += 1; nm = inst.object.name; names[nm] = names.get(nm, 0) + 1
print('INSTANCES', n, list(names.items())[:5])
h = [o for o in bpy.data.objects if o.name.startswith('hedge')][0]
ps = h.evaluated_get(dg).particle_systems[0]
print('PARTICLES', len(ps.particles), ps.settings.render_type, ps.settings.instance_object, leafp.hide_render, leafp.hide_viewport)
k = 0
for inst in dg.object_instances:
    if inst.is_instance and inst.object.name.startswith('leafproto'):
        print('LEAF', inst.matrix_world.to_translation(), inst.matrix_world.to_scale()); k += 1
        if k > 3: break
print('LEAFCOUNT', sum(1 for i in dg.object_instances if i.is_instance and i.object.name.startswith('leafproto')))
