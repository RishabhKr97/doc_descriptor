console.log(window.location.href)
console.log("ooho")
chrome.storage.local.get(['contributions'], function(result) {
    if(result.contributions){
        chrome.storage.local.set({'contributions': (Number(result.contributions)+1)}, function() {
            console.log('Updated contributions to ' + (Number(result.contributions)+1));
        });
    } else {
        chrome.storage.local.set({'contributions': 1}, function() {
            console.log('Updated contributions to 1');
        });
    }
});;