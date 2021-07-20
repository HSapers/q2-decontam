#   Copyright 2021 Evan Bolyen
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import shutil
import pkg_resources
import distutils.dir_util as dir_util

import jinja2

# style tip: stdlib at the top, then 3rd party deps, then QIIME 2, then self.
from q2_reveal.format_types import RevealSectionsDirFmt, RevealSectionsFormat

# Collection package local data can be difficult. Fortunately, pkg_resources
# exists to make this a little less painful than it would have otherwise been
# The rule for the module path is that anything with an __init__.py will be
# delimited with a period. Then the directory that isn't a python subpackage
# will be the last argument.
ASSETS = pkg_resources.resource_filename('q2_decontam.actions', 'assets')

# Set up a template enviornment with the same "style" of module pathing.
J_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader('q2_decontam.actions', 'jinja2')
)


def render(output_dir: str, slides: RevealSectionsDirFmt) -> None:
    # A visualizer takes as its first argument `output_dir` this should have
    # the annotation of `str`. It must be this exact parameter name.
    # This will be a directory in which you should write all of your output,
    # which is why the return annotation for the entire function is set to None
    # (the return annotation may also be ommited).

    # Copying the contents of a directory (rather than the directory itself)
    # is often annoying in Python, distutils has a utility for it.
    dir_util.copy_tree(ASSETS, output_dir)
    dir_util.copy_tree(str(slides.path / 'assets'),
                       os.path.join(output_dir, 'assets'))
    # Lookup our template via Jinja's template environment
    index = J_ENV.get_template('template.html')

    # Convert the "slides" directoryformat attribute to a RevealSectionsFormat
    # Which basically means: "just give me the boring filepath itself".
    ff = slides.slides.view(RevealSectionsFormat)
    # Open is a utility on these FileFormat objects, (you could also use normal
    # open with ff.path or str(ff) depending on your preference for filepath
    # objects
    with ff.open() as slides_fh, \
         open(os.path.join(output_dir, 'index.html'), 'w') as output_fh:

        output_fh.write(
            index.render(content=slides_fh.read())
        )

    # That's it! We copied some assets into the output_dir, and then rendered
    # our template as index.html in the root of output_dir. Interfaces will
    # start by looking for index.html in the root and go from there.


