<?php
    $course_id = $_GET['course_id'];
    $class_id = $_GET['class_id'];
    $section_id = $_GET['section_id'];
?>  

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Vue.JS-->
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <!-- Custom CSS -->    
    <title>Upload Course Materials</title>
</head>
<body>
    <input type='hidden' id='course_id' value='<?=$course_id?>'>
    <input type='hidden' id='class_id' value='<?=$class_id?>'>
    <input type='hidden' id='section_id' value='<?=$section_id?>'>
    <div id='app'>
        <!-- NAV BAR -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
                <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Link</a>
            </li>
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Dropdown
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" href="#">Action</a>
                <a class="dropdown-item" href="#">Another action</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#">Something else here</a>
                </div>
            </li>
            <li class="nav-item">
                <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li>
            </ul>
            <form class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
        </div>
        </nav>
        <!-- END OF NAV BAR -->
        <div class="container">
        <div class="row">
                <div class="col">
                    <div class="jumbotron">
                        <p>Please download and review the following course materials for this section.</p>
                        <ul id='course_materials'></ul>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="jumbotron">
                        <p>To move on, you need to take the quiz and get it 100% correct.</p>
                        <a :href='takeQuiz_link'><button id='startQuizBtn' type="button" class="btn btn-primary">Start Quiz</button></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>

        var app = new Vue({
            el: '#app',
            data: {
                "course_id": '',
                "class_id": '', 
                "section_id": '', 
                "takeQuiz_link": 'Engineer_takeQuiz.php?quiz_id=',
                "user_id": 1 // Hardcoded
            },
            methods: {
                getQuizID: async function() {
                    let url = 'http://localhost:5000/getSectionQuizID'
                    const response = await fetch(url,
                    {
                        method: "POST",
                        headers: {
                           "Content-type": "application/json"
                        },
                        body: JSON.stringify({"course_ID": this.course_id, "class_ID": this.class_id, "section_ID": this.section_id})
                    })

                    if (!response.ok) {
                        console.log("Error getting Quiz ID")
                    }
                    else {
                        const data = await response.json()
                        this.takeQuiz_link += data['quiz_id'] + "&user_id=" + this.user_id
                        this.getCourseMaterials();
                    }
                },
                getCourseMaterials: async function() {
                    let url = "http://localhost:5000/engineer/getCourseMaterials?course_id=" + this.course_id + "&class_id=" + this.class_id + "&section_id=" + this.section_id
                    const response = await fetch(url,{method: "GET"})
                    if (!response.ok) {
                        console.log("Error getting course materials")
                    }
                    else {
                        const data = await response.json()
                        let course_materials_ul = document.getElementById("course_materials")
                        console.log(data)
                        for (cm of data['course_materials']) {
                            console.log(course_materials_ul)
                            course_materials_ul.innerHTML += `<li>
                                        <a href='http://localhost:5000/download?di=`+cm['material_id']+`&name=`+cm['material_name']+`'>`+cm['material_name']+`</a>
                                    </li>`
                        }

                    }
                }
            },
            created: function() {
                this.course_id = document.getElementById("course_id").value;
                this.class_id = document.getElementById("class_id").value;
                this.section_id = document.getElementById("section_id").value;
                this.getQuizID();
            }
        });
    </script>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
</body>
</html>