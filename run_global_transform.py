import gradio as gr
#import cv2
import numpy as np
import math

# Function to convert 2x3 affine matrix to 3x3 for matrix multiplication
def to_3x3(affine_matrix):
    return np.vstack([affine_matrix, [0, 0, 1]])

# Function to apply transformations based on user inputs
def apply_transform(image, scale, rotation, translation_x, translation_y, flip_horizontal):

    # Convert the image from PIL format to a NumPy array
    image = np.array(image)
    # Pad the image to avoid boundary issues
    pad_size = min(image.shape[0], image.shape[1]) // 2
    image_new = np.zeros((pad_size*2+image.shape[0], pad_size*2+image.shape[1], 3), dtype=np.uint8) + np.array((255,255,255), dtype=np.uint8).reshape(1,1,3)
    image_new[pad_size:pad_size+image.shape[0], pad_size:pad_size+image.shape[1]] = image
    
    y0=pad_size+image.shape[0]//2
    x0=pad_size+image.shape[1]//2
    
    transformed_image = np.array(image_new)

    ### FILL: Apply Composition Transform 
    transformed_image[:,:]=[255,255,255]
    for y, x in np.ndindex(transformed_image.shape[:2]):
        y1=y-translation_y
        x1=x-translation_x
        r1=math.sqrt((x1-x0)**2+(y1-y0)**2)
        r1=r1/scale
        theta1=math.atan2(y1-y0,x1-x0)
        theta1=theta1-math.radians(rotation)
        y1=y0+r1*math.sin(theta1)
        x1=x0+r1*math.cos(theta1)
        
        y1=int(y1)
        x1=int(x1)
        if y1-pad_size>=0 and y1-pad_size<image.shape[0] and x1-pad_size>=0 and x1-pad_size<image.shape[1]:
            if not flip_horizontal:
                transformed_image[y,x]=image[y1-pad_size,x1-pad_size]
            else:
                transformed_image[y,x]=image[y1-pad_size,image.shape[1]-1-x1+pad_size]

      


        
        

    # Note: for scale and rotation, implement them around the center of the image （围绕图像中心进行放缩和旋转）

    return transformed_image

# Gradio Interface
def interactive_transform():
    with gr.Blocks() as demo:
        gr.Markdown("## Image Transformation Playground")
        
        # Define the layout
        with gr.Row():
            # Left: Image input and sliders
            with gr.Column():
                image_input = gr.Image(type="pil", label="Upload Image")

                scale = gr.Slider(minimum=0.1, maximum=2.0, step=0.1, value=1.0, label="Scale")
                rotation = gr.Slider(minimum=-180, maximum=180, step=1, value=0, label="Rotation (degrees)")
                translation_x = gr.Slider(minimum=-300, maximum=300, step=10, value=0, label="Translation X")
                translation_y = gr.Slider(minimum=-300, maximum=300, step=10, value=0, label="Translation Y")
                flip_horizontal = gr.Checkbox(label="Flip Horizontal")
            
            # Right: Output image
            image_output = gr.Image(label="Transformed Image")
        
        # Automatically update the output when any slider or checkbox is changed
        inputs = [
            image_input, scale, rotation, 
            translation_x, translation_y, 
            flip_horizontal
        ]

        # Link inputs to the transformation function
        image_input.change(apply_transform, inputs, image_output)
        scale.change(apply_transform, inputs, image_output)
        rotation.change(apply_transform, inputs, image_output)
        translation_x.change(apply_transform, inputs, image_output)
        translation_y.change(apply_transform, inputs, image_output)
        flip_horizontal.change(apply_transform, inputs, image_output)

    return demo

# Launch the Gradio interface
interactive_transform().launch()
