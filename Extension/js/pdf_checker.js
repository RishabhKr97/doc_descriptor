console.log(window.location.href)
link = window.location.href

const Http = new XMLHttpRequest();
const url='http://localhost:5000/pdf_link?url='+link;
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
    // console.log("CHANGE "+Http.readyState);
    if(Http.readyState == 4 && Http.status == 201){
        console.log("READY 4");
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
    }
}
