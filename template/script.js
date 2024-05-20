function updateGrade(id) {
    const studentName = $('#studentName').val();
    const courseName = $('#courseName').val();
    const score = parseFloat($('#score').val());

    const data = {
        'student_name': studentName,
        'course_name': courseName,
        'score': score
    };

    $.ajax({
        type: 'PUT',
        url: `http://localhost:5003/grades/${id}`,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            alert('Grade updated successfully');
        },
        error: function(xhr, status, error) {
            alert('Error: ' + error);
        }
    });
}

function deleteGrade(id) {
    $.ajax({
        type: 'DELETE',
        url: `http://localhost:5003/grades/${id}`,
        success: function(response) {
            alert('Grade deleted successfully');
        },
        error: function(xhr, status, error) {
            alert('Error: ' + error);
        }
    });
}
