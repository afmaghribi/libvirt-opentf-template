
#!/usr/bin/env python3
import os, yaml
from jinja2 import Environment,FileSystemLoader
from bcrypt import hashpw,gensalt

def render_tf_file(specs):
    template_file = Environment(loader=FileSystemLoader("./templates")).get_template("main.tf.j2")
    
    output = open("./main.tf","w")
    output.write(template_file.render(specs))
    output.close()

if __name__ == "__main__": 
    config = yaml.safe_load(open("tf-specs.yaml","r"))
    render_tf_file(config['tf_specs'])