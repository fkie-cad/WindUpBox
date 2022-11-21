# external imports
import attrs

# configure logging
import logging
log = logging.getLogger(__name__)


@attrs.define
class SynchronousCommand:
    command: str
    description: str
    order: str = attrs.field(converter=str, default=0)

    def change_order_number(self, order: int):
        self.order = str(order)
