chrome.storage.local.get(['contributions'], function(result) {
    if(result.contributions){
        console.log("Got "+ result.contributions +" contributions.")
        $("#num_contributions").html(result.contributions + " Contributions");
    }
});