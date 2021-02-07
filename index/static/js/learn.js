		var countNewWord = 0;
		var correctAnswers = 0;
		var wrongAnswers = 0;
		items = new Array;
		items[0] = new Array();
		items[1] = new Array();
		{% for i in newWord %}
		items[0].push("{{i.Definition}}")
		items[1].push("{{i.Term}}")
		{% endfor %}
		/*Random tro choi */
		function randomGameParent(){
			arrRandomGame = new Array;
			arrRandomGame[0] =  new Array("write", "choice");
			function randomGame(items)
			{
				var random = Math.floor(Math.random()*items.length)
				var value = items[random]
				items.splice(random, 1);
				return value;
			}
			var randomGame = randomGame(arrRandomGame[0]);
			if(randomGame == "write")
			{
				document.getElementById("write").style.display = "block";
				document.getElementById("choice").style.display = "none";
				displayWrite();
			}
			if(randomGame == "choice")
			{
				document.getElementById("choice").style.display = "block";
				document.getElementById("write").style.display = "none";
				learn();
			}
		}
		randomGameParent();

		function learn()
		{	
	// Display thanh New words remaining
	var remaining = Math.ceil(countNewWord / items[0].length * 100)
	document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:" + remaining + "%");
	document.getElementsByClassName("progress-bar")[0].innerText = remaining + "%";
			// Đổi màu quay trở lại ban đầu
			var button_mean = document.getElementsByClassName("button_mean");
			for(var i = 0; i < button_mean.length; i++)
			{
				button_mean[i].style.backgroundColor = "#ecf0f1";
			}
			function random_item(items)
			{
				var random = Math.floor(Math.random()*items.length)
				var value = items[random]
				items.splice(random, 1);
				return value;
			}
			function random_4_word(items)
			{
				var random = Math.floor(Math.random()*items.length)
				var value = items[random]
				items.splice(random, 1);
				return value;
			}

			items[0] = new Array();
			items[1] = new Array();
			//Array 3 là nguyên bản nghĩa của các từ tiếng anh không bị chỉnh sửa, mảng này dùng để kiểm tra kết quả người
			items[3] = new Array();
			{% for i in newWord %}
			items[0].push("{{i.Definition}}")
			items[1].push("{{i.Term}}")
			items[3].push("{{i.Term}}")
			{% endfor %}


			// Display new word
			document.getElementById("newWord").innerText = items[0][countNewWord];
			console.log(items[0][countNewWord]);
			// Tạo ra một mảng mới chứa từ có nghĩa đúng
			items[2] = new Array(items[1][countNewWord])
			// xóa từ có nghĩa đúng ra khỏi mảng
			items[1].splice(countNewWord, 1);
			// Thêm 3 từ ngẫu nhiên còn lại vào trong mảng
			for(var i = 0; i < 3; i++){
				items[2].push(random_item(items[1]))
			}
			// xáo trộn 4 từ trong mảng 2 với nhau và sau đó hiển thị lên màn hình
			for(var i = 0; i < 4; i++){
				document.getElementsByClassName("button_mean")[i].innerText = random_4_word(items[2]);
			}
		}
		function check(mean)
		{
			var button_mean = document.getElementsByClassName("button_mean");
			// chuyển màu cho button chứa nghĩa đúng
			for(var i = 0; i < button_mean.length; i++)
			{
				if(button_mean[i].innerText == items[3][countNewWord])
				{
					button_mean[i].style.backgroundColor = "#3498db";
				}
			}
			if(items[3][countNewWord] == mean)
			{
				correctAnswers++;
				// Hien thi cau tra loi dung
				document.getElementById("correctAnswers").innerText = correctAnswers;
				countNewWord ++;
				if(countNewWord < items[0].length)
				{
					setTimeout(learn, 1000);
				}
				else
				{
					// Display thanh New words remaining
					var remaining = Math.ceil(countNewWord / items[0].length * 100)
					document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:" + remaining + "%");
					document.getElementsByClassName("progress-bar")[0].innerText = remaining + "%";
					setTimeout(end, 1000);
				}
				randomGameParent();
			}
			else
			{

				wrongAnswers++;
				document.getElementById("wrongAnswers").innerText = wrongAnswers;
				countNewWord++; 
				if(countNewWord < items[0].length)
				{
					setTimeout(learn, 1000);
					
				}
				else
				{
					// Display thanh New words remaining
					var remaining = Math.ceil(countNewWord / items[0].length * 100)
					document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:" + remaining + "%");
					document.getElementsByClassName("progress-bar")[0].innerText = remaining + "%";
					setTimeout(end, 3000);
				}
				randomGameParent();
			}
		}
		/*function cua write*/
		function checkWrite()
		{
			var inputWrite = document.getElementById('answerWrite').value;
			if(items[1][countNewWord] == inputWrite)
			{
				correctAnswers++;
				countNewWord++;
				document.getElementById("correctAnswers").innerText = correctAnswers;
				randomGameParent();
			}
			else
			{
				wrongAnswers++;
				countNewWord++;
				document.getElementById("wrongAnswers").innerText = wrongAnswers;
				randomGameParent();
			}
			document.getElementById('answerWrite').value = "";
			setTimeout(displayWrite, 1000);
		}
		function displayWrite()
		{
	// Display thanh New words remaining
	var remaining = Math.ceil(countNewWord / items[0].length * 100);
	document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:" + remaining + "%");
	document.getElementsByClassName("progress-bar")[0].innerText = remaining + "%";
	if(countNewWord == items[0].length)
	{
		setTimeout(end, 500);
	}
	else
	{
		//display new word
		document.getElementById('newWord_write').innerText = items[0][countNewWord];
	}
}

function end()
{
	alert("Chúc mừng bạn đã hoàn thành khóa học")
	location.reload();
}
