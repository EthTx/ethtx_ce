#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .abc import SemanticSubmoduleAbc
from .helpers.utils import get_eth_price
from ...models.decoded_model import TransactionMetadata


class SemanticMetadataDecoder(SemanticSubmoduleAbc):
    """ Semantic Metadata Decoder. """

    def decode(self, tx_metadata: TransactionMetadata) -> TransactionMetadata:
        """ Semantically decode metadata. """
        tx_metadata.eth_price = get_eth_price()

        return tx_metadata
