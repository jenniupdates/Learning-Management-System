<!--First, based on the trainer's ID, the page should load the courses that the trainer is teaching-->
<!--Next, clicking view Course should bring the trainer to another page that allows them to edit the Sections-->
<!--To edit a different Course, they will have to press a return to homepage button-->
<!--Within each Section edit page, they should be able to add and delete Sections-->
<?php

$course_id = $_GET['course_id'];
$class_id = $_GET['class_id'];

?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Trainers</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <!-- Vue.JS-->
   <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
   <!-- Bootstrap CSS -->
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
  </head>
<body>
    <input type='hidden' id='course_id' value='<?=$course_id?>'>
    <input type='hidden' id='class_id' value='<?=$class_id?>'>
    <div id="app">
        <h1 class="text-center">Course Sections</h1>
        <h2 class="font-weight-bold text-center">{{course_id}} - Class {{class_id}}</h2>
        <h3 class="text-center">{{user_name}}</h3>
        <h3 class="text-center">My Trainer: {{trainer_name}}</h3>

        <table class="table">
            <thead>
                <thead class="thead-dark">
                    <tr>
                        <th>Section ID</th>
                        <th>Section Description</th>
                        <th>Enter Section</th>
                        <th>Section Quiz</th>
                        <th>Sextion Status</th>
                    </tr>
                </thead>
                <tbody id="section_list">

                </tbody>
                <br>
               
            </thead>
        </table>
        
        <a v-bind:href="final_url"><button type="button" class="btn btn-warning">Take Final Quiz</button></a>
        
    </div>

</form>

    <script>
        var app = new Vue({
            el: '#app',
            data: {
                'sections': [],
                'trainer_name': "Isaac", // Need to Fix
                'course_id': 'Loading...',
                'class_id': 'Loading...',
                'user_name': 'Richard', // Hardcoded for demo
                'user_id' : '1', // Hardcoded for Demo,
                'final_quiz_id': '',
                'final_url': '',
                'status_btn': {'completed': 'badge-success', 'incomplete': 'badge-warning', 'unavailable':'badge-secondary'}
            },
            methods: {
                getAllSections: async function(){
                    let url = 'http://localhost:5000/users/getClassSections?user_id=' + this.user_id + '&course_id=' + this.course_id + '&class_id=' + this.class_id
                    console.log(url)
                    const response = await fetch(url, {method: 'GET'});
                    if(!response.ok){
                        console.log('Error in retrieving getAllSections')
                    }
                    else {
                        const data = await response.json();
                        console.log(data);
                        let status_btn = this.status_btn
                        document.getElementById('section_list').innerHTML = '';
                        for (s of data["sections"]){
                            if (s['section_status'] != 'unavailable') {
                                section_id = s['section_id']
                                course_material = s['course_material']
                                view_sections_btn = `<a href='Engineer_CourseSection.php?course_id=`+this.course_id+`&class_id=`+this.class_id+`&section_id=`+section_id+`'><button type="button" class="btn btn-primary">View</button></a>`
                                quiz_id = s['quiz_id']
                                description = s['description']
                                section_status = s['section_status']
                                let slist = document.getElementById('section_list')
                                slist.innerHTML += 
                                `
                                <tr>
                                    <td>`+section_id+`</td>
                                    <td>`+description+`</td>
                                    <td>`+view_sections_btn+`</td>
                                    <td><a href='Engineer_takeQuiz?quiz_id=`+quiz_id+`&user_id=`+this.user_id+`'><button type="button" class="btn btn-info">Take Quiz</button></a></td>
                                    <td><h5><span class="badge `+status_btn[section_status]+`">`+section_status+`</span></h5></td>
                                </tr>
                                `
                                
                            }
                        }
                        this.sections = data["sections"]
                    }
                }
            },
            created: function() {
                this.course_id = document.getElementById("course_id").value;
                this.class_id = document.getElementById("class_id").value;
                this.final_quiz_id = this.course_id+"-"+this.class_id+"-"+"Final"
                this.final_url = "Engineer_takeQuiz.php?quiz_id=" + this.final_quiz_id + "&user_id=" + this.user_id
                this.getAllSections();
            }
        });

    </script>
  
</body>
</html>