from Sketchformer.sketchformer_api import *

simplified_sketch = []

image = [[284, 205, 0], [282, 203, 0], [281, 202, 0], [279, 201, 0], [277, 198, 0], [276, 197, 0], [274, 195, 0], [273, 194, 0], [271, 193, 0], [270, 191, 0], [269, 190, 0], [267, 188, 0], [266, 187, 0], [264, 186, 0], [263, 185, 0], [262, 184, 0], [259, 184, 0], [258, 183, 0], [257, 183, 0], [255, 183, 0], [252, 184, 0], [250, 185, 0], [248, 186, 0], [245, 187, 0], [243, 188, 0], [241, 189, 0], [240, 191, 0], [238, 191, 0], [237, 193, 0], [236, 194, 0], [234, 196, 0], [233, 197, 0], [232, 198, 0], [232, 200, 0], [232, 201, 0], [232, 202, 0], [232, 204, 0], [232, 205, 0], [232, 206, 0], [232, 207, 0], [233, 209, 0], [235, 211, 0], [235, 212, 0], [237, 213, 0], [239, 215, 0], [241, 216, 0], [243, 217, 0], [245, 219, 0], [247, 219, 0], [248, 219, 0], [250, 220, 0], [250, 221, 0], [247, 223, 0], [245, 224, 0], [242, 226, 0], [237, 228, 0], [235, 229, 0], [232, 231, 0], [231, 232, 0], [229, 234, 0], [228, 235, 0], [227, 236, 0], [226, 238, 0], [226, 239, 0], [226, 241, 0], [226, 242, 0], [226, 245, 0], [226, 246, 0], [226, 249, 0], [228, 250, 0], [229, 253, 0], [230, 255, 0], [232, 256, 0], [233, 258, 0], [234, 259, 0], [236, 261, 0], [238, 262, 0], [239, 263, 0], [241, 264, 0], [243, 265, 0], [244, 266, 0], [247, 266, 0], [249, 266, 0], [250, 266, 0], [251, 266, 0], [253, 266, 0], [254, 266, 0], [255, 266, 0], [256, 265, 0], [256, 264, 0], [257, 264, 0], [256, 266, 0], [254, 269, 0], [252, 272, 0], [251, 275, 0], [250, 280, 0], [250, 283, 0], [250, 285, 0], [251, 287, 0], [253, 290, 0], [254, 291, 0], [256, 294, 0], [257, 295, 0], [260, 297, 0], [262, 298, 0], [265, 300, 0], [270, 302, 0], [275, 302, 0], [282, 303, 0], [289, 303, 0], [296, 302, 0], [301, 302, 0], [308, 300, 0], [314, 298, 0], [320, 296, 0], [323, 294, 0], [325, 293, 0], [326, 290, 0], [328, 289, 0], [328, 288, 0], [329, 286, 0], [329, 285, 0], [329, 284, 0], [329, 282, 0], [330, 284, 0], [331, 285, 0], [332, 287, 0], [334, 290, 0], [336, 291, 0], [338, 292, 0], [341, 294, 0], [344, 296, 0], [346, 296, 0], [349, 296, 0], [351, 296, 0], [354, 296, 0], [359, 294, 0], [362, 292, 0], [367, 290, 0], [370, 289, 0], [372, 287, 0], [375, 285, 0], [376, 282, 0], [378, 279, 0], [379, 275, 0], [380, 273, 0], [380, 269, 0], [380, 265, 0], [379, 262, 0], [379, 260, 0], [378, 259, 0], [378, 258, 0], [379, 258, 0], [381, 258, 0], [384, 258, 0], [387, 257, 0], [390, 255, 0], [395, 253, 0], [398, 252, 0], [400, 250, 0], [402, 249, 0], [404, 247, 0], [405, 246, 0], [407, 244, 0], [407, 241, 0], [408, 237, 0], [408, 234, 0], [408, 229, 0], [408, 226, 0], [407, 223, 0], [405, 219, 0], [403, 215, 0], [401, 213, 0], [399, 211, 0], [396, 209, 0], [394, 208, 0], [392, 206, 0], [390, 205, 0], [387, 204, 0], [386, 203, 0], [385, 203, 0], [384, 203, 0], [384, 201, 0], [383, 199, 0], [382, 197, 0], [381, 196, 0], [380, 194, 0], [379, 192, 0], [377, 190, 0], [376, 188, 0], [374, 187, 0], [373, 186, 0], [371, 184, 0], [369, 183, 0], [367, 182, 0], [364, 180, 0], [361, 180, 0], [358, 180, 0], [355, 180, 0], [351, 180, 0], [349, 180, 0], [347, 181, 0], [346, 182, 0], [344, 183, 0], [343, 185, 0], [341, 186, 0], [341, 187, 0], [340, 189, 0], [339, 189, 0], [338, 188, 0], [337, 186, 0], [335, 184, 0], [333, 181, 0], [332, 179, 0], [330, 177, 0], [329, 174, 0], [327, 173, 0], [326, 172, 0], [324, 170, 0], [323, 170, 0], [321, 168, 0], [320, 167, 0], [319, 167, 0], [317, 167, 0], [315, 167, 0], [311, 168, 0], [309, 170, 0], [307, 171, 0], [305, 173, 0], [303, 174, 0], [300, 176, 0], [299, 177, 0], [297, 179, 0], [296, 180, 0], [295, 181, 0], [293, 182, 0], [293, 183, 0], [291, 184, 0], [291, 185, 0], [290, 187, 0], [289, 189, 0], [289, 190, 0], [289, 191, 0], [288, 193, 0], [287, 193, 0], [287, 194, 0], [287, 195, 0], [287, 196, 0], [286, 196, 0], [286, 197, 0], [286, 198, 0], [286, 199, 0], [286, 200, 0], [287, 200, 0], [287, 201, 0], [287, 202, 0], [288, 202, 1]]

temp_arr = [[],[]]
model = get_model()

image = apply_RDP(image)
image = normalize(image)
simplified_sketch.append(image)
object_lists = predict(model, simplified_sketch)
print(object_lists)