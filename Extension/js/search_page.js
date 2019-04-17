$('#start-search').click(function(){
    var query = '?';
    $('.choices__item--selectable').each(function(){
        query += 'query='+$(this).attr('data-value')+'&';
    });
    console.log(query);
    window.location = "search_result.html"+query;
});
