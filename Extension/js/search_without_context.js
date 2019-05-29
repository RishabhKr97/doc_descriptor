// OBJECT STRUCTURE
// {
//     "title": " ",
//     "published_on": " " (UTC timestamp),
//     "authors": [" ", " "],
//     "summary": " ",
//     "web_link": " ",
//     "download_link": " ",
//     "tags": [" ", " "]
// }

var TEST_RESULT = [{"paper_id": 3520, "authors": ["Dmitrij Schlesinger"], "published_on": 1509321600, "title": "A Connection between Feed-Forward Neural Networks and Probabilistic\n  Graphical Models", "summary": "Two of the most popular modelling paradigms in computer vision are\nfeed-forward neural networks (FFNs) and probabilistic graphical models (GMs).\nVarious connections between the two have been studied in recent works, such as\ne.g. expressing mean-field based inference in a GM as an FFN. This paper\nestablishes a new connection between FFNs and GMs. Our key observation is that\nany FFN implements a certain approximation of a corresponding Bayesian network\n(BN). We characterize various benefits of having this connection. In\nparticular, it results in a new learning algorithm for BNs. We validate the\nproposed methods for a classification problem on CIFAR-10 dataset and for\nbinary image segmentation on Weizmann Horse dataset. We show that statistically\nlearned BNs improve performance, having at the same time essentially better\ngeneralization capability, than their FFN counterparts.", "tags": ["ML", "CV", "LG"], "web_link": "http://arxiv.org/abs/1710.11052v1", "download_link": "http://arxiv.org/pdf/1710.11052v1"},
{"paper_id": 3519, "authors": ["Masaya Hibino", "Akisato Kimura", "Takayoshi Yamashita", "Yuji Yamauchi", "Hironobu Fujiyoshi"], "published_on": 1509321600, "title": "Denoising random forests", "summary": "This paper proposes a novel type of random forests called a denoising random\nforests that are robust against noises contained in test samples. Such\nnoise-corrupted samples cause serious damage to the estimation performances of\nrandom forests, since unexpected child nodes are often selected and the leaf\nnodes that the input sample reaches are sometimes far from those for a clean\nsample. Our main idea for tackling this problem originates from a binary\nindicator vector that encodes a traversal path of a sample in the forest. Our\nproposed method effectively employs this vector by introducing denoising\nautoencoders into random forests. A denoising autoencoder can be trained with\nindicator vectors produced from clean and noisy input samples, and non-leaf\nnodes where incorrect decisions are made can be identified by comparing the\ninput and output of the trained denoising autoencoder. Multiple traversal paths\nwith respect to the nodes with incorrect decisions caused by the noises can\nthen be considered for the estimation.", "tags": ["CV", "LG", "ML"], "web_link": "http://arxiv.org/abs/1710.11004v1", "download_link": "http://arxiv.org/pdf/1710.11004v1"}]

function append_result(obj, counter){
    var new_elem = '<div class="';

    if(counter%2 == 0) new_elem += 'blog-card">'
    else new_elem += 'blog-card alt">'

    new_elem += '<div class="meta">'+
                    '<div class="photo" style="background-image: url(images/background'+counter%6+'.jpg)">'+
                    '</div>'+
                    '<ul class="details">'+
                        '<li class="author"><a href="#">'+obj['authors'][0]+' et. al.</a></li>'+
                        '<li class="date">'+new Date(Number(obj['published_on'])*1000).toDateString()+'</li>';
                        // if(obj['tags'].length > 0){
                            new_elem += '<li class="tags">'+
                                            '<ul>';
                            // for(var i=0; i<obj['tags'].length; i++){
                            //     new_elem +=     '<li><a href="#">'+obj['tags'][i]+'&nbsp;</a></li>';
                            // }
                            new_elem +=     '<li><a href="#">'+'SCORE = '+obj['score']+'&nbsp;</a></li>';
                            new_elem +=     '</ul>'+
                                        '</li>';
                        // }
        new_elem += '</ul>'+
                '</div>'+
                '<div class="description">'+
                    '<h1>'+obj['title']+'</h1>'+
                    '<h2>';
                    for(var i=0; i<obj['authors'].length-1; i++){
                        new_elem += obj['authors'][i]+', ';
                    }
                    new_elem += obj['authors'][obj['authors'].length - 1] +
                    '</h2>'+
                    '<p style="text-align: justify">'+obj['summary'].split(" ").splice(0,50).join(" ")+'...</p>'+
                    '<p class="read-more">'+
                        '<a href="'+obj['download_link']+'">Read More</a>'+
                    '</p>'+
                '</div>'+
            '</div>';
    $("#body").append(new_elem);
}

// $('#test').click(function(){
//     for(var i=0; i<10; i++){
//         append_result(TEST_RESULT[i%2], i);
//     }
// });

// for(var i=0; i<10; i++){
//         append_result(TEST_RESULT[i%2], i);
// }

const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.getAll('query');
console.log(query);
const Http = new XMLHttpRequest();
const url='http://localhost:5000/search_no_context?q='+query.join(" ");
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
    if(Http.readyState == 4 && Http.status == 200){
        console.log("READY 4");
        var jsonResponse = JSON.parse(Http.responseText);
        for(var i=0; i<jsonResponse.length; i++){
            append_result(jsonResponse[i], i);
        }
    }
}
