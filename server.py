from flask import Flask, Response, request
import json,os,random, random,string

def random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


app = Flask(__name__,template_folder="templates")
app.secret_key = random_string(random.randint(1,30))

from PIL import Image

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def resize_image(image_path,w,h):
    image = Image.open(image_path)
    new_size = (w,h)
    resized_image = image.resize(new_size)
    resized_image.save('compressed_image.jpg', optimize=True, quality=50)
    return 'compressed_image.jpg'

def image_to_pixel_list(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixel_list = []
    i = 0
    for y in range(height):
        for x in range(width):
            i += 1
            pixel = img.getpixel((x, y))
            pixel_list.append(rgb_to_hex(pixel[0],pixel[1],pixel[2]))

    os.remove(image_path)
    return pixel_list

@app.route("/list", methods=["GET"])
def list():
    return generate_response(200,"Response",os.listdir("images"))

@app.route("/api", methods=["POST"])
def api():
    body = request.get_json()
    print(body)
    pixel_list = image_to_pixel_list(resize_image(body["image"],body["width"],body["height"]))
    response_dict = {"pixel_list":pixel_list}
    return generate_response(200,"Response",response_dict)
            
def generate_response(status, name, content, message=False):
    body = {}
    body[name] = content
    if message:
        body["message"] = message
    return Response(json.dumps(body), status=status, mimetype="application/json")
        

app.run(debug=True)
