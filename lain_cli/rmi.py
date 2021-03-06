# -*- coding: utf-8 -*-
from argh.decorators import arg

import lain_sdk.mydocker as docker
from lain_cli.utils import (check_phase, get_domain, ClusterConfig,
                            get_meta_versions_from_tags, lain_yaml)


def get_repo_tags_to_remove(registry):
    yml = lain_yaml(ignore_prepare=True)
    all_tags = docker.get_tag_list_in_docker_daemon(registry, yml.appname)
    using_tags = docker.get_tag_list_using_by_containers(registry, yml.appname)
    using_meta_versions = get_meta_versions_from_tags(using_tags)
    tags_to_keep = []
    for version in using_meta_versions:
        tags_to_keep.extend([
            "meta-%s" % (version),
            "release-%s" % (version)
        ])
    tags_to_delete = []
    for tag in all_tags:
        if tag not in tags_to_keep and tag not in tags_to_delete:
            tags_to_delete.append(tag)
    return ["%s/%s:%s" % (registry, yml.appname, t) for t in tags_to_delete]


@arg('phase', help="lain cluster phase id, can be added by lain config save")
@arg('-r', '--registry', help='registry url')
def rmi(phase, registry=None):
    """
    Remove app images in the local host
    """

    check_phase(phase)
    params = dict(name=phase)
    if registry is not None:
        params['registry'] = registry

    cluster_config = ClusterConfig(**params)
    repo_tags = get_repo_tags_to_remove(cluster_config.registry)
    for image in repo_tags:
        docker.remove_image(image)
