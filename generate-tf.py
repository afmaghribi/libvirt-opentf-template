
#!/usr/bin/env python3
import os, yaml
from jinja2 import Environment,FileSystemLoader
from bcrypt import hashpw,gensalt

def render_cloud_init(specs):
    template_file = Environment(loader=FileSystemLoader("./templates")).get_template("user-data.j2")
    
    for vms in (specs['vm_specs']):
        vms['hashed_password'] = hashpw(vms['password'].encode(), gensalt()).decode()

        if "pub_key" not in specs.keys():
            key_path = os.path.expanduser('~/.ssh/id_rsa.pub')
            vms["pub_key"] = open(key_path,"r").read().strip()
            vms["priv_key"] = key_path[:-4]
        elif "ssh-rsa" not in vms["pub_key"]:
            vms["pub_key"] = open(vms["pub_key"],"r").read().strip()
            vms["priv_key"] = vms["pub_key"][:-4]

        if not os.path.isdir("./generated"):
            os.makedirs("./generated")

        output = open("./generated/"+vms['hostname']+"-user-data.cfg","w")
        output.write(template_file.render(vms))
        output.close()

def render_network_config(specs):
    template_file = Environment(loader=FileSystemLoader("./templates")).get_template("network-config.j2")

    for vms in (specs['vm_specs']):
        output = open("./generated/"+vms['hostname']+"-network-config.cfg","w")
        output.write(template_file.render(vms))
        output.close()

def render_tf_file(specs):
    template_file = Environment(loader=FileSystemLoader("./templates")).get_template("main.tf.j2")
    
    output = open("./main.tf","w")
    output.write(template_file.render(specs))
    output.close()

if __name__ == "__main__": 
    config = yaml.safe_load(open("tf-specs.yaml","r"))
    render_cloud_init(config['tf_specs'])
    render_network_config(config['tf_specs'])
    render_tf_file(config['tf_specs'])