<!--First, based on the trainer's ID, the page should load the courses that the trainer is teaching-->
<!--Next, clicking view Course should bring the trainer to another page that allows them to edit the Sections-->
<!--To edit a different Course, they will have to press a return to homepage button-->
<!--Within each Section edit page, they should be able to add and delete Sections-->
<?php
    $course_id = $_GET['course_id'];
    $class_id = $_GET['class_id'];
    if (isset($_GET['trainer_name'])) {
        $trainer_name =  $_GET['trainer_name'];
    }
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Edit Course</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <!-- Vue.JS-->
   <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
   <!-- Bootstrap CSS -->
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
   <style>
       #app{
           padding: 20px 20px;
       }
    </style>
  </head>
<body>
    <!-- NAV BAR -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">LMS Trainer</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item">
            <a class="nav-link" href="Trainer_Homepage2.html">Homepage</a>
        </li>
        <li class="nav-item">
          <a class="dropdown-item" href="../">Change Demo Role</a>
        </li>
        </ul>
    </div>
    </nav>
<!-- END OF NAV BAR -->
    <input type='hidden' id='course_id' value='<?=$course_id?>'>
    <input type='hidden' id='class_id' value='<?=$class_id?>'>
    <input type='hidden' id='trainer_name' value='<?=$trainer_name?>'>

    <div id="app">
        <h1 class="text-center">Course Sections</h1>
        <h2 class="font-weight-bold text-center">{{course_id}} - Class {{class_id}}</h2>
        <h3 class="text-center">{{trainer_name}}</h3>

        <table class="table">
            <thead>
                <thead class="thead-dark">
                    <tr>
                        <th>Section ID</th>
                        <th>Section Description</th>
                        <th>Course Materials</th>
                        <th>Section Quiz</th>
                    </tr>
                </thead>
                <tbody id="section_list">

                </tbody>
            </thead>
        </table>
        <!--Add a Course Section button-->
        <div class="form-group">
            <label for="new_description">Description</label>
            <input type="text" class="form-control" id="new_description" placeholder="Enter section description">
        </div>
        <button type="button" class="btn btn-primary" @click='addNewSection()'>Add a New Section</button>
        <br><br>
        <div class v-if="final_quiz_id.length > 0">
            <button type="button" class="btn btn-primary" v-on:click="createFinalQuiz">Edit {{final_quiz_id}}</button>
        </div>
        <div class v-else>
            <button type="button" class="btn btn-primary" v-on:click="createFinalQuiz">Create Final Quiz</button>
        </div>
        <br>
        <div style ="text-align:center;">
            <a href='Trainer_Homepage2.html'><button type="button" class="btn btn-info">Back to Homepage</button></a>
        </div>
    </div>
</form>

    <script>
        var app = new Vue({
            el: '#app',
            data: {
                'sections': [],
                'trainer_name': '',
                'course_id': '',
                'class_id': '',
                'name': '',
                'last_id': 0,
                'final_quiz_id': '',
                'quiz_id': '',
                'page_url': ''
            },
            methods: {
                getAllSections: async function(){
                    let class_id = this.class_id
                    let course_id = this.course_id
                    let last_id = this.last_id
                    let url = 'http://3.23.147.209:5000/trainers/getAllSections?course_id=' + course_id + '&class_id=' + class_id
                    let section_list = document.getElementById('section_list')
                    section_list.innerHTML = ''
                    const response = await fetch(url, {method: 'GET'});
                    if(!response.ok){
                        console.log("Error in retrieving getAllSections")
                    }
                    else {
                        const data = await response.json();
                        let section_list = document.getElementById('section_list')
                        for (section of data["sections"]){
                            section_id = section["section_id"]
                            description = section["description"]
                            quiz_id = section["quiz_id"]
                            course_material = ''
                            upload_id = course_id + "-" + class_id + "-" + section['section_id']
                            // Create empty button in initialized section for uploading course materials
                            if(section["course_materials"].length > 0) {
                                course_material = `<ul>`
                                for (material of section['course_materials']) {
                                    course_material += `<li>
                                        <a href='http://3.23.147.209:5000/download?di=`+material['material_id']+`&name=`+material['name']+`'>`+material['name']+`</a>
                                    </li>`
                                }
                                course_material += `
                                </ul>`
                            }

                            course_material += `
                            <form action = "http://3.23.147.209:5000/uploader?ui=`+upload_id+`&class_id=`+this.class_id+`&trainer_name=`+this.trainer_name+`&url='`+this.page_url+`'" method = "POST"
                            enctype = "multipart/form-data">
                            <input type = "file" name = "file"/> <input type = "submit"/>
                            `
                        
                            // Create empty button in initialized section for creating quiz if empty 
                            // and Edit Quiz button if there is already a quiz
                            if (section["quiz_id"] != null){
                                quiz_button = `
                                <button type='button' class='btn btn-primary' onclick="editQuiz('`+quiz_id+`')">Edit Quiz</button>
                                `
                            }
                            else {
                                quiz_button = `
                                <button type='button' class='btn btn-primary' onclick="createQuiz('`+course_id+`', '`+class_id+`', '`+section_id+`')">Create Quiz</button>
                                `
                            }
                            
                            section_list.innerHTML += `
                                <tr>
                                    <td>`+section_id+`</td>
                                    <td>`+description+`</td>
                                    <td>`+course_material+`</td>
                                    <td>`+quiz_button+`</td>
                                </tr>   
                            `
                            this.last_id++;
                        }
                        this.sections = data["sections"]
                        this.getFinalQuiz();
                    }
                },
                addNewSection: async function(){
                    let new_description = document.getElementById("new_description").value;
                    let last_id = this.last_id;
                    last_id++;
                    // Update the database with the new section
                    let url = "http://3.23.147.209:5000/trainers/updateSections?section_id=" + last_id + "&description=" + encodeURI(new_description) + "&course_id=" + this.course_id + "&class_id=" + this.class_id;
                    const response = await fetch(url, {method: 'GET'});
                    if(!response.ok){
                        console.log("Error in updating the database with new section")
                    }
                    else{
                        const data = await response.json()
                        console.log("Successful update")
                    }
                    // Reflect the changes by calling on getAllSections gain
                    this.getAllSections();
                },
                createFinalQuiz: async function(){
                    if (this.final_quiz_id.length > 0){
                        window.location.replace("Trainer_CreateQuiz.html?quiz_id=" + this.final_quiz_id + "&status=edit&trainer_name=" + app.trainer_name)
                    }
                    else{
                        this.final_quiz_id = this.course_id + "-" + this.class_id + "-" + "Final"
                        window.location.replace("Trainer_CreateQuiz.html?quiz_id=" + this.final_quiz_id + "&status=create&trainer_name=" + app.trainer_name)
                    }
                    
                },
                getFinalQuiz: async function(){
                    let url = "http://3.23.147.209:5000/trainers/getFinalQuiz?course_id="+ this.course_id + "&class_id=" + this.class_id
                    const response = await fetch(url, {method: 'GET'});
                    if(!response.ok){
                        console.log("Error in getting final quiz idn")
                    }
                    else{
                        const data = await response.json()
                        if (data["final_quiz_id"] != null){
                            this.final_quiz_id = data["final_quiz_id"]
                        }
                    }
                }
            },
            created: function() {
                this.page_url = window.location.href
                console.log(this.page_url)
                this.course_id = document.getElementById("course_id").value
                this.class_id = document.getElementById("class_id").value
                this.trainer_name = document.getElementById("trainer_name").value
                this.getAllSections();
            }
        });

        async function editQuiz(quiz_id){
            console.log("[START] of editing a quiz");
            console.log(quiz_id);
            window.location.replace("Trainer_CreateQuiz.html?quiz_id=" + quiz_id + "&status=edit&trainer_name=" + app.trainer_name)
            // send the quiz_id to the trainer edit quiz sections
        }

        async function createQuiz(course_id, class_id, section_id){
            console.log("[START] of creating a quiz");
            let quiz_id = course_id + "-" + class_id + "-" + section_id
            console.log(quiz_id)
            window.location.replace("Trainer_CreateQuiz.html?quiz_id=" + quiz_id + "&status=create&trainer_name=" + app.trainer_name)
            // send the quiz i to the trainer create quiz html
        }
    </script>
  
</body>
</html>