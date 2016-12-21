var degree = 0;

// Quando a página termina de carregar:
$(document).ready(function() {
    // Evento de click no botão (id="rotateright")
    $(document).on('click','#rotateright',function(){
        degree += 0.1;
        // Seletor (.val) salva em degree
        $("#degree").val(degree);
        // Seletor (.css) muda o css de image
        $("#image").css({'transform': 'rotate('+ degree + 'deg)'});
    });

    $(document).on('click','#rotateleft',function(){
        degree -= 0.1;
        $("#degree").val(degree);
        $("#image").css({'transform': 'rotate(' + degree + 'deg)'});
    });

    $(document).on('click','#confirm',function(){
        var img_path = $("#img_path").val();
        var degree = $("#degree").val();
        $.post(route, {img_path: img_path, degree: degree},function(data, status){
            // Seletor (.html) muda todo o conteudo da div id = "new-img"
            $("#new-img").html("<img src=\" " + data.url + "?v=" + Math.random() + "\">");
        });
    });
});
