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

import lxml.etree

from q2_decontam.plugin_setup import plugin
from q2_decontam.format_types import RevealSectionsFormat


@plugin.register_transformer
def _0(ff: RevealSectionsFormat) -> lxml.etree._Element:
    with ff.open() as fh:
        return lxml.etree.fromstring(fh.read())


@plugin.register_transformer
def _1(data: lxml.etree._Element) -> RevealSectionsFormat:
    ff = RevealSectionsFormat()
    # Need to use the `.path` because lxml produces Bytes rather than Strings.
    with ff.path.open(mode='w+b') as fh:
        fh.write(lxml.etree.tostring(data))

    return ff
