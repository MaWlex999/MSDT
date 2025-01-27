class LinkManager:
    def __init__(self):
        self.links = []

    def add_link(self, link_id, items, total):
        if any(link["link_id"] == link_id for link in self.links):
            raise ValueError("Link ID already exists")
        if total < 0:
            raise ValueError("Total cannot be negative")
        self.links.append({"link_id": link_id, "items": items, "total": total})

    def get_link(self, link_id):
        for link in self.links:
            if link["link_id"] == link_id:
                return link
        raise ValueError("Link not found")

    def remove_link(self, link_id):
        for link in self.links:
            if link["link_id"] == link_id:
                self.links.remove(link)
                return
        raise ValueError("Link not found")

    def calculate_total_links(self):
        return sum(link["total"] for link in self.links)