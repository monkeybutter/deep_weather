/*
Copyright 2015 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

"use strict";

function getMaps() {
    document.getElementById("rain").src = "http://127.0.0.1:3000/map?type=rain&date=" + document.getElementById("date").value + "&param=none"
    document.getElementById("z500").src = "http://127.0.0.1:3000/map?type=weather&date=" + document.getElementById("date").value + "&param=z500"
    document.getElementById("z850").src = "http://127.0.0.1:3000/map?type=weather&date=" + document.getElementById("date").value + "&param=z850"
    document.getElementById("ta700").src = "http://127.0.0.1:3000/map?type=weather&date=" + document.getElementById("date").value + "&param=ta700"

    console.log(document.getElementById("date").value)
}

function oneForward() {
	var dateStr = document.getElementById("date").value;
	var date = new Date(Date.parse(dateStr))
	console.log(date.toISOString());
	var newDate = new Date();
	newDate.setTime(date.getTime() + (6 * 3600 * 1000));
	var newISOdateStr = newDate.toISOString();
	var newdateStr = newISOdateStr.substring(0, newISOdateStr.length-5);
	console.log(newdateStr);
	document.getElementById("date").value = newdateStr;
	getMaps();
}

function oneBack() {
		var dateStr = document.getElementById("date").value;
	var date = new Date(Date.parse(dateStr))
	console.log(date.toISOString());
	var newDate = new Date();
	newDate.setTime(date.getTime() - (6 * 3600 * 1000));
	var newISOdateStr = newDate.toISOString();
	var newdateStr = newISOdateStr.substring(0, newISOdateStr.length-5);
	console.log(newdateStr);
	document.getElementById("date").value = newdateStr;
	getMaps();
}
