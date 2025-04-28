class CityMap:
    def __init__(self, resources_by_type: dict):
        # Store the raw data
        self.graph = resources_by_type

    def _address_allowed(self, ranges, addr):
        if ranges == "all":
            return True
        for r in ranges:
            if r[0] <= addr <= r[1]:
                return True
        return False

    def _get_next_node(self, current: str):
        entity_id = current['entity_id']
        if 'house' in entity_id:
            return self.graph['house'][entity_id]['neighborhood']
        elif 'nbh' in entity_id:
            return self.graph['neighborhood'][entity_id]['exits']
        elif 'junction' in entity_id:
            return s elf.graph['junction'][entity_id]['exits']



    def get_path(self, src_id: str, dst_id: str) -> list[str]:
        """ get path base on the graph """
        visited = set()
        final_path = []
        current = src_id
        while final_path[-1] != dst_id:
            next_node = self._get_next_node(current)
