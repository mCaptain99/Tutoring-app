function refreshPage(page) {
    var newUrl = `${window.location.origin}${window.location.pathname}?${$('form').serialize()}&page=${page}`
    window.location.href = newUrl;
    return true;
}