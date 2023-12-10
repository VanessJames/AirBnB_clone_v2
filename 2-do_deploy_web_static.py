#!/usr/bin/python3
""" a function"""

from fabric.api import local, run, env, put
from datetime import datetime as time
from os import path


env.hosts = ["ubuntu@52.201.211.152", "ubuntu@35.174.184.32"]


def do_pack():
    """do pack function """
    try:
        time_stamp = time.now().strftime("%Y%m%d%H%M%S")
        saved_path = "versions/web_static_{}.tgz".format(
            time_stamp
        )
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(
            saved_path
        ))
    except Exception:
        return None
    else:
        return saved_path


def do_deploy(archive_path):
    """ do deploy function"""
    try:
        if not path.exists(archive_path):
            return False

        releases = "/data/web_static/releases"
        web_static_dir = path.basename(archive_path).split(".")[0]

        put(local_path=archive_path, remote_path="/tmp/")

        run("rm -rf {}/{}".format(
            releases,
            web_static_dir
        ))

        run("mkdir -p {}/{}".format(
            releases,
            web_static_dir
        ))
        run("tar -xzf /tmp/{}.tgz -C {}/{}".format(
            web_static_dir,
            releases,
            web_static_dir
        ))

        run("rm -f /tmp/{}.tgz".format(
            web_static_dir
        ))

        run("mv {0}/{1}/web_static/* {0}/{1}".format(
            releases,
            web_static_dir,
        ))

        run("rm -rf {}/{}/web_static".format(
            releases, web_static_dir
        ))

        run("rm -rf /data/web_static/current")

        run("ln -s {}/{}/ /data/web_static/current".format(
            releases, web_static_dir
        ))

        print("New version deployed!")
        return True

    except Exception:
        return False
