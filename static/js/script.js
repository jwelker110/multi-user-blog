(function(){
    "use strict";

    var likeBtn = document.getElementById('like-btn');
    var likeForm = document.getElementById('like-form');
    if (!likeBtn) { return; }
    likeBtn.addEventListener('click', function(e){
        if (likeForm) {
            likeForm.submit();
        }
    });

})();
