        function parseparams(num){

                tempstring='/QA_demo/?question_type='+num;
                count =1;
                $( 'input[class=\"input-large inputbox'+num+'\"]' ).each(function() {
                tempstring+='&param'+ count +'='+encodeURIComponent($(this).val());
                count+=1;
                });
                    window.location=tempstring;
                }

        $('#myCollapsible').collapse({
        toggle: false
        })


        $('#tablist a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        })


        $("#John").hover(function() {
              $("#result h2").text("John Ellenberger");
               $("#role").text("Supervisor");
               $("#title").text("Director SAP Research");
                $("#address").text("SAP Labs LLC, 3 Van de Graaff Drive, Burlington, MA 01803");
                $("#email").text("john.ellenberger@sap.com");
                $("#phone").text("T +1 781 852 8945, M +1 978 421 5176");})

        $("#Puntis").hover(function() {
              $("#result h2").text("Puntis Jifroodian");
               $("#role").text("NLP");
               $("#title").text("Intern- SAP Research");
                $("#address").text("SAP Labs Montreal, 111 Duke Street, Montreal, Quebec, H3C 2M1, Canada");
                $("#email").text("puntis.jifroodian-haghighi@sap.com");
                $("#phone").text("");})


        $("#Alexis").hover(function() {
              $("#result h2").text("Alexis Tremblay");
               $("#role").text("NLP-SQL Backend");
               $("#title").text("Intern- SAP Research");
                $("#address").text("SAP Labs Montreal, 111 Duke Street, Montreal, Quebec, H3C 2M1, Canada");
                $("#email").text("alexis.tremblay@sap.com");
                $("#phone").text("T +1 (514) 228-2181");})

        $("#Caitlin").hover(function() {
              $("#result h2").text("Caitlin Mehl");
               $("#role").text("GUI");
               $("#title").text("Intern- SAP Research");
                $("#address").text("SAP Labs, Inc. - Boston 245 First Street, 16th Floor Cambridge, MA 02142 USA");
                $("#email").text("caitlin.mehl@sap.com");
                $("#phone").text("T +1 617 715 7326");})

