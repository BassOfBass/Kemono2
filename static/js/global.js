function add_url_param(url, param_name, param_value) {
    var url = new URL(url);
    url.searchParams.set(param_name, param_value);
    return url.toString();
}
