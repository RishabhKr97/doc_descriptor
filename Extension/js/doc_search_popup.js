chrome.storage.local.get(['contributions'], function(result) {
    if(result.contributions){
        console.log("Got "+ result.contributions +" contributions.")
        $("#num_contributions").html(result.contributions + " Contributions");
    }
});

$("#web_page_button").click(function(){
    chrome.tabs.create({
        url: "search_page.html"
    });
});

$("#search_string").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#search_button").click();
    }
});

$("#search_button").click(function(){
    console.log($("#search_string").val());
    var query = $("#search_string").val();
    chrome.tabs.create({
        url: "search_result.html?query="+query
    });
});