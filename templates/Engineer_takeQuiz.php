<?php
    if (isset($_GET['quiz_id'])) {  
        $quiz_id = $_GET['quiz_id'];
        $user_id = $_GET['user_id'];
    }
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
            <input type='hidden' id='quiz_id' value='<?= $quiz_id ?>'>
            <input type='hidden' id='user_id' value='<?= $user_id ?>'>
            <h1 class='text-center'>Quiz</h1>
            <div id="quiz">
            </div>
            <div class="row">
                <div class="col">
                    <div class="jumbotron">
                        <h4 id='result_percent'></h4>
                        <button id='submitBtn' type="button" class="btn btn-success" @click='gradeQuiz'>Submit Quiz</button> <br>
                        <small id='small'>Once you submit your answers, you cannot change them!</small> <br><br>
                        <div class="row">
                            <div class="col">
                                <div id="nextSection"></div>
                            </div>
                            <div class="col">
                                <div id="retakeQuiz"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script type='text/javascript'>

        var app = new Vue({
            el: '#app',
            data: {
                'quiz_id': null,
                'quiz_data': null,
                'user_id': null

            },
            methods: {
                getQuizQuestionsAndOptions: async function() {
                    let url = 'http://localhost:5000/getQuestionsAndOptions/' + this.quiz_id
                    const response = await fetch(url, {method: 'GET'});
                    if (!response.ok) {
                        console.log("Error retrieving Quiz Questions & Options");
                    }
                    else {
                        const quiz_data = await response.json();
                       // console.log(quiz_data['quiz'])
                       q_count = 1
                        let quiz = document.getElementById("quiz");
                        for (question of quiz_data['quiz']) {
                            //console.log(question)
                            let q_name = question['question_name']
                            let q_num = "Q" + q_count
                            let choice_id = "choices" + q_count
                            let alert_id = "alert" + q_count
                            quiz.innerHTML += `
                            <div class="row">
                                <div class="col">
                                    <div class="jumbotron" id='`+q_num+`'>
                                        <div id='`+alert_id+`'></div>
                                        <h5>`+q_num+`) `+q_name+`</h5>
                                        <div id='`+choice_id+`'>
                                        </div>
                                    </div>
                                </div>
                            </div>`
                            let choices = document.getElementById(choice_id)
                            c_count = 1
                            for (option of question['options']) {
                                //console.log(option)
                                let radio_id = q_num + "C" + c_count
                                let radio_name = q_num
                                choices.innerHTML += `
                                <div class="custom-control custom-radio">
                                    <input id="`+radio_id+`" type="radio" name="`+radio_name+`" class="custom-control-input" value='`+option+`'>
                                    <label class="custom-control-label" for="`+radio_id+`">`+option+`</label>
                                </div>`
                                c_count += 1

                            }

                            q_count += 1
                        }
                    }
                },
                gradeQuiz: async function() {
                    document.getElementById("submitBtn").setAttribute("disabled",true)
                    let quiz_answers = []
                    let quiz = document.getElementById("quiz")
                    let jumbotron_list = quiz.getElementsByClassName("jumbotron");
                    //console.log(jumbotron_list)
                    for (element of jumbotron_list) {
                        //console.log(element)
                        let question_id = element.id.substr(1)
                        //console.log(question_id)
                        let question_obj = {"question_id": question_id, "answer": null}
                        let options = element.getElementsByClassName("custom-control-input")
                        for (option of options) {
                            //console.log(option)
                            if (option.checked) {
                                question_obj.answer = option.value
                            }
                        }
                        quiz_answers.push(question_obj)
                        
                    }
                    let url = 'http://localhost:5000/gradeQuiz'
                    const response = await fetch(url,
                    {
                        method: "POST",
                        headers: {
                           "Content-type": "application/json"
                        },
                        body: JSON.stringify({
                            "quiz_id": this.quiz_id,
                            "submission": quiz_answers
                        })
                    });

                    if (!response.ok) {
                        console.log("Error calling gradeQuiz")
                    }
                    else {
                        // COMPLETE THIS
                        const data = await response.json();
                        let no_correct = 0
                        for (let i=0;i<data['quiz_results'].length;i++) {
                            question_id = i + 1
                            cur_alert_id = "alert" + question_id
                            let alert_div = document.getElementById(cur_alert_id)
                            if (data['quiz_results'][i]['correct?'] == "No") {
                                alert_div.innerHTML = `<div class="alert alert-danger" role="alert">
                                                            Wrong! The correct answer is `+data['quiz_results'][i]['correct_answer']+`
                                                        </div>`
                            }
                            else {
                                alert_div.innerHTML = `<div class="alert alert-success" role="alert">
                                                            Correct!
                                                        </div>`
                                no_correct += 1
                            }
                            
                        }
                        let score_percent = no_correct / data['quiz_results'].length * 100
                        document.getElementById("result_percent").innerText = "Your Score: " + score_percent + "%"
                        this.completeSection();
                        document.getElementById("retakeQuiz").innerHTML = `<button type="button" class="btn btn-secondary" onclick='retakeQuiz()'>Retake Quiz</button>`
                    }
                },
                completeSection: async function() {
                    let quiz_id_split = this.quiz_id.split("-")
                    let course_id = quiz_id_split[0]
                    let class_id = quiz_id_split[1]
                    let section_id = quiz_id_split[2]
                    let url = "http://localhost:5000/engineer/completeSection"
                    const response = await fetch(url,
                    {
                        method: "POST",
                        headers: {
                           "Content-type": "application/json"
                        },
                        body: JSON.stringify({
                            "course_id": course_id,
                            "class_id": class_id,
                            "section_id": section_id,
                            "user_id": this.user_id,
                        })
                    });
                    if (!response.ok) {
                        console.log("Error completing the section")
                    }
                    else {
                        this.makeNextSectionAvl(course_id,class_id,section_id,this.user_id)
                    }
                    
                },
                makeNextSectionAvl: async function(course_id,class_id,cur_section_id,user_id) {
                    let url = 'http://localhost:5000/engineer/makeNextSectionAvl'
                    let small = document.getElementById("small")
                    const response = await fetch(url,
                    {
                        method: "POST",
                        headers: {
                           "Content-type": "application/json"
                        },
                        body: JSON.stringify({
                            "course_id": course_id,
                            "class_id": class_id,
                            "section_id": cur_section_id,
                            "user_id": this.user_id,
                        })
                    });
                    if (!response.ok) {
                        console.log("Error making next section available")
                    }
                    else {
                        const data = await response.json()
                        if (data['next?'] == "yes") {
                            let link = `Engineer_CourseSection.php?course_id=`+course_id+`&class_id=`+class_id+`&section_id=`+data['next_section_id']
                            small.innerText = data['message']
                            document.getElementById("nextSection").innerHTML = `<a href='`+link+`'><button type="button" class="btn btn-info">Proceed to Next Section</button></a>`
                        }
                        else {
                            small.innerText = data['message']
                            document.getElementById("nextSection").innerHTML = `<a href=''><button type="button" class="btn btn-warning">Take Final Quiz</button></a>`
                        }
                    }
                }
            },

            created: function() {
                this.user_id = document.getElementById("user_id").value;
                this.quiz_id = document.getElementById("quiz_id").value;
                this.getQuizQuestionsAndOptions();

            }
        });

        function retakeQuiz(){
            window.location.reload();
        }
    </script>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
</body>
</html>