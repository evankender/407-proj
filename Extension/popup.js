document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('link');
    link.addEventListener('click', function() {
      chrome.tabs.query({active:true,currentWindow:true},function(tab){

        var jsonURL = 'http://0.0.0.0:5000/getPageData?url=' + tab[0].url;
        fetch(jsonURL)
        .then(res => res.json())
        .then((out) => {
          console.log('Checkout this JSON! ', out);
        })
        .catch(err => { throw err });

      });
    });
});
