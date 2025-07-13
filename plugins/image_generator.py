from PIL import Image, ImageDraw

def generate_mockup(args, context):
    product_info = args["product_info"]
    filename = "mockup.png"
    
    img = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 250), product_info["title"], fill="black")
    img.save(filename)
    
    product_info["image"] = filename
    return product_info
