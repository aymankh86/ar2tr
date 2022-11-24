$(document).ready(function () {
    $(".page-link").click(function() {
        var direction = $(this).data("direction");
        var currentUrl = window.location.href;
        var url = new URL(currentUrl);
        var currentPage = url.searchParams.get("page") || 1;
        currentPage = parseInt(currentPage)
        var nextPage = currentPage;
        if (direction == 'next') {
            nextPage = currentPage + 1
        } else if (direction == 'prev') {
            nextPage = currentPage - 1
        }
        url.searchParams.set("page", nextPage);
        var newUrl = url.href; 
        window.location = newUrl;
    })
   
    $(".ar2tr-searchform").submit(function (event) {
        var searchFromText = $(".ar2tr-searchform-textbox").val().toLowerCase();
        var category = $("#select-category").val().toLowerCase();
        if (searchFromText.length == 0 && !category)
            return false;
    });

    $( "#searchTerm2" ).autocomplete({
        source: function(request, response) {
            $.getJSON("/search",{query:request.term},response);
        },
        minLength: 1,
        select: function(event, ui) {            
              console.log(event)
        },
    });

    $(".searchResultsTable tr .rc4").click(function(){
        $("#edit-category").val($(this).data("category"))
        $("#ar-phrase").val($(this).data("ar"))
        $("#tr-phrase").val($(this).data("tr"))
        $("#type").val($(this).data("edit"))
        $("#id").val($(this).data("id"))
        $("#exampleModal").modal('show');
    });

    $("#save").click(function() {
        var cat = $("#edit-category").val();
        var ar = $("#ar-phrase").val();
        var tr = $("#tr-phrase").val();
        var type = $("#type").val();
        var id = $("#id").val();
        if (!cat || !ar || !tr) {
            $("#error-msg").text("يرجى ملئ جميع الحقول")
            $("#error-msg").show()
            return false;
        }
        var data = {category: cat, ar_text: ar, tr_text: tr, job_type: type, phrase: id}
        $.post("/suggest", data)
        .done(function(data) {
            $("#success-msg").show()
            $("#error-msg").hide()
        })
        .fail(function(xhr, status, error) {
            $("#success-msg").hide()
            $("#error-msg").show()
        })
    })

    $('#exampleModal').on('hidden.bs.modal', function (e) {
        $("#success-msg").hide()
        $("#error-msg").hide()
    })


    let voices = []
    const hasSynth = 'speechSynthesis' in window

    if (hasSynth) {
        voices = speechSynthesis.getVoices()
        speechSynthesis.addEventListener('voiceschanged', () => {
        voices = speechSynthesis.getVoices()
        })
    }

    $(".fa-volume-up").click(function() {
        var text = $(this).data("text");
        
        if (!voices.length && hasSynth) {
        voices = speechSynthesis.getVoices()
        } 
        
        voices.forEach(voice => {
        if (voice.name == 'Yelda'){
            if (hasSynth) {
            const utterance = new SpeechSynthesisUtterance()
        
            utterance.text = text
            utterance.voice = voice
            utterance.rate = 0.8;
            speechSynthesis.speak(utterance)
            }
        }
        })

    });
});