#!/usr/bin/python3
"""
Fabfile to distribute an archive to a web server.
execute: fab -f 2-do_deploy_web_static.py do_deploy:\
    archive_path=folder/file.tgz -i ssh_key -u user
"""
from os import path

# from dotenv import load_dotenv
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import local

env.hosts = ["52.201.211.152", "35.174.184.32"]
env.user = "ubuntu"
env.key_filename = "~/.ssh"

run_locally = True


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    local("cp {} /tmp/{}".format(archive_path, file))
    local("rm -rf /data/web_static/releases/{}/".format(name))
    local("mkdir -p /data/web_static/releases/{}/".format(name))
    local("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
    local("rm /tmp/{}".format(file))
    local(
        "mv /data/web_static/releases/{}/web_static/*"
        " /data/web_static/releases/{}/".format(name, name)
    )
    local("rm -rf /data/web_static/releases/{}/web_static".format(name))
    local("rm -rf /data/web_static/current")
    local("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if (
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)
        ).failed
        is True
    ):
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if (
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name)
        ).failed
        is True
    ):
        return False
    if (
        run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed
        is True
    ):
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if (
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)
        ).failed
        is True
    ):
        return False

    print("New version deployed!")
    return True
