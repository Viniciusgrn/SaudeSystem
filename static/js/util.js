(function () {
    /*
    $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
        }
        
        var $subMenu = $(this).next(".dropdown-menu");
        $subMenu.toggleClass('show');
        
        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
            $('.dropdown-submenu .show').removeClass("show");
        });    
    
        return false;
    });*/

    // procedimento = $('#id_procedimento');
    
    // procedimento.on('change', ()=>{
    //     var procedimento = $("#id_procedimento");
    //     console.log(procedimento);
    //     var botao = $("#btnEnviar");
    //     console.log(botao);
    //     if (procedimento == "procedimento") {   
    //         console.log('entrei papai');
    //         botao.disabled = false;
    //         procedimento.style.border="2px solid red";
    //     } else {
    //         console.log('entrei mamãe');            
    //         botao.disabled = true;
    //         procedimento.css({"border-color": "2px solid green"});
    //     }
    // });
    
    /*if (!document.getElementById("id_dum")) {
        var dumInput = document.getElementById('id_dum');
        var igInput = document.getElementById('id_idadeGestacional');
        var somaSemanasInput = document.getElementById('id_somaSemanas');
        var somaDiasInput = document.getElementById('id_somaDias');
        var dppTag = document.getElementById('id_dpp');
        var semanasTag = document.getElementById('semanas');
        var diasTag = document.getElementById('dias');
        var trimestreTag = document.getElementById('trimestre');
        
        dumInput.addEventListener('change', function(){
            if(dumInput.value.length == 10){
                calcularDpp(dumInput.value);
            }
        });

        somaSemanasInput.addEventListener('change', function(){
            if(dumInput.value.length == 10){
                calcularDpp(dumInput.value);
            }
        });

        somaDiasInput.addEventListener('change', function(){
            if(dumInput.value.length == 10){
                calcularDpp(dumInput.value);
            }
        });    

        function calcularDpp(dum){
            const dataDum = new Date(dum);
            if (isNaN(dataDum.getTime())) {
                document.getElementById('resultado').innerHTML = "Por favor, insira uma data válida.";
                return;
            }

            // Calcular a DPP (280 dias após a DUM)
            const dataProvavelParto = new Date(dataDum.getTime());
            dataProvavelParto.setDate(dataDum.getDate() + ((280 - somaSemanasInput.value * 7) - somaDiasInput.value ));
            
            
            // Calcular a diferença em semanas e dias
            const hoje = new Date();
            
            const somaSemanas = somaSemanasInput.value ? (somaSemanasInput.value * 7 * 24 * 60 * 60 * 1000) : 0;
            const somaDias = somaDiasInput.value ? (somaDiasInput.value * 24 * 60 * 60 * 1000) : 0;
            
            const diferenca = hoje - dataDum;
            let dataAjustada = diferenca + somaSemanas + somaDias;
            const quantidadeSemanas = Math.floor(dataAjustada / (1000 * 60 * 60 * 24 * 7));
            const quantidadeDias = Math.floor((dataAjustada / (1000 * 60 * 60 * 24)) % 7);
            
            // Determinar o trimestre da gravidez        
            let quantidadeTrimestre;
            if (quantidadeSemanas < 13) {
                quantidadeTrimestre = "1º Trim";
            } else if (quantidadeSemanas < 27) {
                quantidadeTrimestre = "2º Trim";
            } else {
                quantidadeTrimestre = "3º Trim";
            }

            if (quantidadeSemanas > 1) {
                semanasTag.innerText = quantidadeSemanas + " semanas";
            } else{
                semanasTag.innerText = quantidadeSemanas + " semana";
            }

            if (quantidadeDias > 1) {
                diasTag.innerText = quantidadeDias + " dias";
            } else {
                diasTag.innerText = quantidadeDias + " dia";
            }

            var dia = Number(dataProvavelParto.toISOString().split('T')[0].substring(8));
            var mes = Number(dataProvavelParto.toISOString().split('T')[0].substring(5,7));
            var ano = Number(dataProvavelParto.toISOString().split('T')[0].substring(0,4));
            
            dppTag.innerText = dia+"/"+mes+"/"+ano;
            trimestreTag.innerText = quantidadeTrimestre;
        }
    }*/



































    
        // Função para inicializar dropdowns
        function initDropdowns() {
            $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
                if (!$(this).next().hasClass('show')) {
                    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
                }
                
                var $subMenu = $(this).next(".dropdown-menu");
                $subMenu.toggleClass('show');
                
                $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
                    $('.dropdown-submenu .show').removeClass("show");
                });    
            
                return false;
            });
        }
    
        // Função para inicializar o procedimento (comentado pois não há detalhes completos)
        function initProcedimento() {
            /*
            var procedimento = $('#id_procedimento');
            
            procedimento.on('change', function() {
                var procedimento = $("#id_procedimento");
                console.log(procedimento);
                var botao = $("#btnEnviar");
                console.log(botao);
                if (procedimento.val() == "procedimento") {   
                    console.log('entrei papai');
                    botao.prop('disabled', false);
                    procedimento.css({"border": "2px solid red"});
                } else {
                    console.log('entrei mamãe');            
                    botao.prop('disabled', true);
                    procedimento.css({"border": "2px solid green"});
                }
            });
            */
        }
    
        // Função para inicializar a DPP
        function initDpp() {
            if (document.getElementById("id_dum")) {
                var dumInput = document.getElementById('id_dum');
                var igInput = document.getElementById('id_idadeGestacional');
                var somaSemanasInput = document.getElementById('id_somaSemanas');
                var somaDiasInput = document.getElementById('id_somaDias');
                var dppTag = document.getElementById('id_dpp');
                var semanasTag = document.getElementById('semanas');
                var diasTag = document.getElementById('dias');
                var trimestreTag = document.getElementById('trimestre');
                
                dumInput.addEventListener('change', function(){
                    if(dumInput.value.length == 10){
                        calcularDpp(dumInput.value);
                    }
                });
    
                somaSemanasInput.addEventListener('change', function(){
                    if(dumInput.value.length == 10){
                        calcularDpp(dumInput.value);
                    }
                });
    
                somaDiasInput.addEventListener('change', function(){
                    if(dumInput.value.length == 10){
                        calcularDpp(dumInput.value);
                    }
                });    
    
                function calcularDpp(dum){
                    const dataDum = new Date(dum);
                    if (isNaN(dataDum.getTime())) {
                        document.getElementById('resultado').innerHTML = "Por favor, insira uma data válida.";
                        return;
                    }
    
                    // Calcular a DPP (280 dias após a DUM)
                    const dataProvavelParto = new Date(dataDum.getTime());
                    dataProvavelParto.setDate(dataDum.getDate() + ((280 - somaSemanasInput.value * 7) - somaDiasInput.value ));
                    
                    
                    // Calcular a diferença em semanas e dias
                    const hoje = new Date();
                    
                    const somaSemanas = somaSemanasInput.value ? (somaSemanasInput.value * 7 * 24 * 60 * 60 * 1000) : 0;
                    const somaDias = somaDiasInput.value ? (somaDiasInput.value * 24 * 60 * 60 * 1000) : 0;
                    
                    const diferenca = hoje - dataDum;
                    let dataAjustada = diferenca + somaSemanas + somaDias;
                    const quantidadeSemanas = Math.floor(dataAjustada / (1000 * 60 * 60 * 24 * 7));
                    const quantidadeDias = Math.floor((dataAjustada / (1000 * 60 * 60 * 24)) % 7);
                    
                    // Determinar o trimestre da gravidez        
                    let quantidadeTrimestre;
                    if (quantidadeSemanas < 13) {
                        quantidadeTrimestre = "1º Trim";
                    } else if (quantidadeSemanas < 27) {
                        quantidadeTrimestre = "2º Trim";
                    } else {
                        quantidadeTrimestre = "3º Trim";
                    }
    
                    if (quantidadeSemanas > 1) {
                        semanasTag.innerText = quantidadeSemanas + " semanas";
                    } else{
                        semanasTag.innerText = quantidadeSemanas + " semana";
                    }
    
                    if (quantidadeDias > 1) {
                        diasTag.innerText = quantidadeDias + " dias";
                    } else {
                        diasTag.innerText = quantidadeDias + " dia";
                    }
    
                    var dia = Number(dataProvavelParto.toISOString().split('T')[0].substring(8));
                    var mes = Number(dataProvavelParto.toISOString().split('T')[0].substring(5,7));
                    var ano = Number(dataProvavelParto.toISOString().split('T')[0].substring(0,4));
                    
                    dppTag.innerText = dia+"/"+mes+"/"+ano;
                    trimestreTag.innerText = quantidadeTrimestre;
                }
            }
        }
    
        // Inicializar todas as funções
        function init() {
            initDropdowns();
            initProcedimento();
            initDpp();
        }
    
        // Chamar a função init para inicializar tudo
        $(document).ready(init);
})();
