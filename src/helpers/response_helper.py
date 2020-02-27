def pagination(page, page_size, total_items):
    """
    Pagination for creating metadata
    """
    total_pages = total_items // page_size if total_items % page_size == 0 \
        else (total_items // page_size) + 1
    next_page = page + 1 if page < total_pages else None
    previous_page = page - 1 if (1 < page <= total_pages + 1) else None
    return {
        'current_page': page,
        'page_size': page_size,
        'total_items': total_items,
        'next_page': next_page,
        'previous_page': previous_page,
        'total_pages': total_pages
    }