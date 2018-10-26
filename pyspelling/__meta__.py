"""`PySpelling` package."""

#   (major, minor, micro, release type, pre-release build, post-release build, development-release)
version_info = (1, 0, 0, 'beta', 2, 0)


def pep440_version(vi):
    """
    Get the version (PEP 440).

    Version structure
      (major, minor, micro, release type, pre-release build, post-release build)
    Release names are named is such a way they are sortable and comparable with ease.
      (`.dev-alpha` | `.dev-beta` | `.dev-canidate` | `.dev-final` | `alpha` | `beta` | `candidate` | `final`)

    - pre-releases will have a pre-release build number greater than 0
    - post-release is only applied if post-release build is greater than 0
    - development branches append `.dev-`. You can mark pre, post, or final builds as development.
      All `.dev-` releases are sorted before even `alpha`, with `.dev-alpha` coming first, and `.dev-final` coming last.
    - `.dev` is always appended to the end of the releases string and given the build of 0.
      As we don't manage build releases, `.dev` is more of a way to mark that the current code is development.
      If we were doing regular builds and putting them on a server, then the build number would be more important.

    Acceptable version releases:

    ```
    (1, 0, 0, 'final', 0, 0)      1.0
    (1, 2, 0, 'final', 0, 0)      1.2
    (1, 2, 3, 'final', 0, 0)      1.2.3
    (1, 2, 0, 'alpha', 4, 0)      1.2a4
    (1, 2, 0, 'beta', 4, 0)       1.2b4
    (1, 2, 0, 'candidate', 4, 0)  1.2rc4
    (1, 2, 0, 'beta', 1, 1):      1.2b1.post1
    (1, 2, 0, 'final', 0, 1)      1.2.post1
    (1, 2, 3, '.dev-alpha', 1, 0) 1.2.3a1.dev0
    (1, 2, 3, '.dev-final', 0, 0) 1.2.3.dev0
    (1, 2, 3, '.dev-final', 0, 1) 1.2.3.post1.dev0
    (1, 2, 3, '.dev-beta', 2, 1)  1.2.3b2.post1.dev0
    ```

    """

    # Determine if this is a development build or regular build
    dev, rel_type = (True, vi[3][5:]) if vi[3].startswith('.dev-') else (False, vi[3])

    releases = {"alpha": 'a', "beta": 'b', "candidate": 'rc', "final": ''}

    # Ensure version info is valid.
    # Version info should be proper length.
    assert len(vi) == 6
    # Should be a valid release.
    assert rel_type in releases
    # Pre-release releases should have a pre-release value.
    assert rel_type == 'final' or vi[4] > 0
    # Final should not have a pre-release value.
    assert rel_type != 'final' or vi[4] == 0

    # Assemble major, minor, patch version. Patch can be left out if 0.
    main = '.'.join(str(x) for x in (vi[0:2] if vi[2] == 0 else vi[0:3]))
    # Assemble pre-release if needed.
    prerel = releases[rel_type] + str(vi[4]) if releases[rel_type] else ''
    # Assemble post-release if we have one.
    postrel = '.post%d' % vi[5] if vi[5] > 0 else ''
    # Assemble development release if we have one.
    devrel = '.dev0' if dev else ''

    return ''.join((main, prerel, postrel, devrel))


version = pep440_version(version_info)