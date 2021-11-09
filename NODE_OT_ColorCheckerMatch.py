import bpy
import colorsys

class NODE_OT_ColorCheckerMatch(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "node.colorchecker_match"
    bl_label = "Match Color Checker Colors"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        scene.use_nodes = True        
        tree = context.scene.node_tree
        
        hue_node = tree.nodes.new(type='CompositorNodeHueCorrect')
        hue_node.mapping.use_clip = False
        
        # add 001 at both ends to make it cyclic
        colorchecker_rgb = [scene.colorchecker_001,
            scene.colorchecker_002,
            scene.colorchecker_003,
            scene.colorchecker_004,
            scene.colorchecker_005,
            scene.colorchecker_006,
            scene.colorchecker_007,
            scene.colorchecker_008,
            scene.colorchecker_009,
            scene.colorchecker_010,
            scene.colorchecker_011,
            scene.colorchecker_012,
            scene.colorchecker_013,
            scene.colorchecker_014,
            scene.colorchecker_015,
            scene.colorchecker_016,
            scene.colorchecker_017,
            scene.colorchecker_018,
            scene.colorchecker_019,
            scene.colorchecker_020,
            scene.colorchecker_021,
            scene.colorchecker_022,
            scene.colorchecker_023,
            scene.colorchecker_024,
            scene.colorchecker_001]

        colorchecker_hsv = list(map(colorsys.rgb_to_hsv, colorchecker_rgb))
        
        # plot hue points
        colorchecker_h = [hsv[0] for hsv in colorchecker_hsv]
        
        def hue_y(x, h):
            norm = abs(h - x)
            cyclic = 1 - norm
            if norm < cyclic:
                return norm + 0.5
            return -1 * cyclic + 0.5
        
        hh_points = hue_node.mapping.curves[0].points
        while len(hue_node.mapping.curves[0].points) > 2:
            p = hue_node.mapping.curves[0].points[0]
            hue_node.mapping.curves[0].points.remove(p)
        i = 2
        while i < 25:
            hue_node.mapping.curves[0].points.new((1.0/24)*i,0.5)
            i = i + 1
        for index, h in enumerate(colorchecker_h):
            hue_x = index / 24
            hh_points[index].location = (hue_x, hue_y(hue_x, h))
        
        # plot saturation points
        colorchecker_s = [hsv[1] for hsv in colorchecker_hsv]
        # division by zero so I disabled this part
        # colorchecker_s = [((1.0 / s) / 2.0) for s in colorchecker_s]
        
        hs_points = hue_node.mapping.curves[1].points
        while len(hue_node.mapping.curves[1].points) > 2:
            p = hue_node.mapping.curves[1].points[0]
            hue_node.mapping.curves[1].points.remove(p)
        i = 2
        while i < 25:
            hue_node.mapping.curves[1].points.new((1.0/24)*i,0.5)
        for index, s in enumerate(colorchecker_s):
            hs_points[index].location = (index / 24, s)
        hue_node.mapping.update()
        
        
        return {'FINISHED'}
