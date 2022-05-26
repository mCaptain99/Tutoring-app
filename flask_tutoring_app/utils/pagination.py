class Pagination:
    def __init__(self, page: int, total_count: int, page_size: int):
        """This function init pagination object:
        :param page: page of set of objects
        :param total_count: total count of that set
        :param page_size: size of page
        """
        self.page = page
        self.total_count = total_count
        self.has_next = page_size * page < total_count
        self.has_previous = page > 1
        self.next = page + 1
        self.previous = page - 1
        self.far_from_beginning = page > 2
        self.last_page = total_count//page_size + (total_count % page_size != 0)
        self.far_from_end = page < self.last_page - 1
