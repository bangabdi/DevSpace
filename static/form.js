$(document).ready(function(){
    
    $('form').on('submit', function(event) {

        $.ajax({

            data:{

                title : $('#title').val()
        },

        type : 'POST',
        url:'/process'
        })

        event.preventDefault();

    });
});

