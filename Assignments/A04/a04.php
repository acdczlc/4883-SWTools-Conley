<?php
/* 
Zac Conley
2/23/19
A04.php answers all assignment 4 questions using sql
used your functions from a03.php on github
*/
//Connect to mysql
$host = "localhost";            //add username and password
$user = "*******";        // user name
$password = "*******";         // password 
$database = "nfl_data";             // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


/**
 * This function runs a SQL query and returns the data in an associative array
 * that looks like:
 * $response [
 *      "success" => true or false
 *      "error" => contains error if success == false
 *      "result" => associative array of the result
 * ]
 *
 */
function runQuery($mysqli,$sql){
    $response = [];

    // run the query
    $result = $mysqli->query($sql);

    // If we were successful
    if($result){
        $response['success'] = true;
        // loop through the result printing each row
        while($row = $result->fetch_assoc()){
            $response['result'][] = $row;
        }
        $result->free();
    }else{
        $response['success'] = false;
        $response['error'] = $mysqli->error;
    }

    return $response;
}
function f(){
    ob_flush();
    flush();
}
/**
 * Pulls a player out of players table and returns:
 *     [name] => Player.Name
 * Params:
 *     playerId [string] : id of type => 00-000001234
 * Returns:
 *     name [string] : => T. Smith
 */
function getPlayer($playerId){
    global $mysqli;
    $sql = "SELECT `name` FROM players WHERE id = '{$playerId}' LIMIT 1";
    $response = runQuery($mysqli,$sql); 
    if(!array_key_exists('error',$response)){
        return $response['result'][0]['name'];
    }
    return null;
}
/**
 * Prints a question plus a border underneath
 * Params:
 *     question [string] : "Who ran the most yards in 2009?"
 *     pads [array] : [3,15,15,5] padding for each data field
 * Returns:
 *     header [string] : Question with border below
 */
function printHeader($question,$pads,$cols){
    if(strlen($question) > array_sum($pads)){
        $padding = strlen($question);
    }else{
        $padding = array_sum($pads);
    }
    $header = "\n<b>";
    $header .= "{$question}\n\n";
    for($i=0;$i<sizeof($cols);$i++){
        $header .= str_pad($cols[$i],$pads[$i]);
    }
    $header .= "\n".str_repeat("=",$padding);
    $header .= "</b>\n";
    return $header;
}
/**
 * formatRows:
 *    Prints each row with a specified padding for allignment
 * Params:
 *    $row [array] - array of multityped values to be printed
 *    $cols [array] - array of ints corresponding to each column size wanted
 * Example:
 *    
 *    $row = ['1','00-00000123','T. Smith','329']
 *    $pads = [4,14,20,5]
 */
function formatRows($row,$pads){
    $ouput = "";
    for($i=0;$i<sizeof($row);$i++){
        $output .= str_pad($row[$i],$pads[$i]);
    }
    return $output."\n";
}
/**
 * displayQuery: print question + sql result in a consistent and 
 *               formatted manner
 * Params: 
 *     question [string] : question text
 *     sql [string] : sql query
 *     cols [array] : column headers in array form
 *     pads [array] : padding size in ints for each column
 */
function displayQuery($question,$sql,$cols,$pads){
    global $mysqli;
    $parts = explode('.',$question);
    if($parts[0]%2==0){
        $color="#C0C0C0";
    }else{
        $color = "";
    }
    echo"<pre style='background-color:{$color}'>";
    echo printHeader($question,$pads,$cols);
    $response = runQuery($mysqli,$sql);
    if($response['success']){
        foreach($response['result'] as $id => $row){
            $id++;
            $row['id'] = $id;
            $row['name'] = getPlayer($row['playerid']);
            $row[0] = $row[$cols[0]];
            $row[1] = $row[$cols[1]];
            $row[2] = $row[$cols[2]];
            $row[3] = $row[$cols[3]];
            $row[4] = $row[$cols[4]];
            echo formatRows($row,$pads);
        }
    }
    echo"</pre>";
    f();
}
//start of questions and answers
//header
echo nl2br('Name: Zac Conley
Assignment: A04 - Nfl Stats 
Date: 2/23/2019
==================================================================================');
//start of questions
$question = "1. Find the player(s) that played for the most teams.";
$pads = [8,26,12,5];
$sql = "SELECT id as playerid,name,count(distinct(club)) as count FROM `players` group by id,name ORDER BY `count` DESC LIMIT 5";
$response = runQuery($mysqli,$sql);
$cols = ['id','name','count'];
displayQuery($question,$sql,$cols,$pads);

$question = "2. Top 5 rushers per year.";
$pads = [6,13,15,10,5];
$sql = "(SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2009 group by season,playerid ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards)as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2010 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2011 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2012 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2013 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2014 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2015 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2016 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2017 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5) union all (SELECT playerid,name,players_stats.season,sum(yards) as Rushing_yards FROM `players_stats`join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE ( statid=10 or statid=11 or statid=12 or statid=13) and players_stats.season=2018 group by season,playerid  
ORDER BY `Rushing_yards`DESC limit 5)
";
$response = runQuery($mysqli,$sql);
$cols = ['id','playerid','name','season','Rushing_yards'];
displayQuery($question,$sql,$cols,$pads);

$question = "3. Bottom 5 passers per year.";
$pads = [6,13,15,10,5];
$sql = "(SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2009 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2010 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2011 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2012 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2013 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2014 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2015 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2016 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2017 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)union all (SELECT playerid,name,players_stats.season,sum(yards) as Total_Passing_Yards FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=15 or statid=16 or statid =17 or statid=18) and players_stats.season=2018 group by playerid,season ORDER BY Total_Passing_Yards Asc limit 5)
";
$response = runQuery($mysqli,$sql);
$cols = ['id','playerid','name','season','Total_Passing_Yards'];
displayQuery($question,$sql,$cols,$pads);

$question = "4. Find the top 5 players with most rushes for a loss.";
$pads = [6,13,15,10];
$sql = "SELECT playerid,players.name,count(yards)as rushes_for_loss FROM `players_stats` join players on players_stats.playerid=players.id and players_stats.season=players.season WHERE (statid=10 or statid=11 or statid=12 or statid=13) and yards<0 group by playerid ORDER BY `rushes_for_loss`  DESC limit 5";
$response = runQuery($mysqli,$sql);
$cols = ['id','playerid','name', 'rushes_for_loss'];
displayQuery($question,$sql,$cols,$pads);

$question = "5. Find the top 5 teams with the most penalties.";
$pads = [6,13,15];
$sql = "SELECT club,sum(pen)as total_penalties FROM `game_totals` group by club order by total_penalties desc limit 5";
$response = runQuery($mysqli,$sql);
$cols = ['id','club','total_penalties'];
displayQuery($question,$sql,$cols,$pads);

$question = "6. Find the average number of penalties per year.";
$pads = [6,13,25,16];
$sql = "SELECT season,sum(pen) as total_penalties,sum(pen)/ (count(pen)/2) as avg_penalties_per_game FROM `game_totals` group by season";
$response = runQuery($mysqli,$sql);
$cols = ['id','season','total_penalties','avg_penalties_per_game'];
displayQuery($question,$sql,$cols,$pads);

$question = "7. Find the Team with the least amount of average plays every year.";
$pads = [6,13,25,16];
$sql = "(SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2009' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2010' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2011' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2012' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2013' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2014' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2015' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2016' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2017' group by games.season,clubid order by avg_plays asc limit 1) union all (SELECT games.season,plays.clubid,cast(count(playid)/ count(distinct plays.gameid) as int) as avg_plays FROM `plays` inner join games on plays.gameid=games.gameid where games.season='2018' group by games.season,clubid order by avg_plays asc limit 1)";
$response = runQuery($mysqli,$sql);
$cols = ['id','season','clubid','avg_plays'];
displayQuery($question,$sql,$cols,$pads);

$question = "8. Find the top 5 players that had field goals over 40 yards.";
$pads = [6,18,25];
$sql = "SELECT players.name as kicker, count(players_stats.yards)as FGs FROM `players_stats`inner join players on players_stats.playerid=players.id WHERE players_stats.statid=70 and players_stats.yards>40 group by players_stats.playerid  ORDER BY `FGs`  DESC limit 5";
$response = runQuery($mysqli,$sql);
$cols = ['id','kicker','FGs'];
displayQuery($question,$sql,$cols,$pads);

$question = "9. Find the top 5 players with the shortest avg field goal length.";
$pads = [6,18,25];
$sql = "SELECT players.name as kicker, avg(players_stats.yards)as Shortest_Average_Distance FROM `players_stats`inner join players on players_stats.playerid=players.id WHERE players_stats.statid=70 group by players_stats.playerid  ORDER BY `Shortest_Average_Distance`  aSC limit 5";
$response = runQuery($mysqli,$sql);
$cols = ['id','kicker','Shortest_Average_Distance'];
displayQuery($question,$sql,$cols,$pads);

$question = "10. Rank the NFL by win loss percentage (worst first).";
$pads = [6,18,25];
$sql = "SELECT club,count(wonloss)/160 as wins FROM `game_totals` where wonloss='won' group by club  
ORDER BY `wins`  ASC
";
$response = runQuery($mysqli,$sql);
$cols = ['id','club','wins'];
displayQuery($question,$sql,$cols,$pads);

$question = "11. Find the top 5 most common last names in the NFL.";
$pads = [6,18,25];
$sql = "SELECT SUBSTRING_INDEX(name,'.',-1) AS last_name ,count(distinct id)as occurrences from players where name like '__%' group by last_name order by occurrences desc limit 5
";
$response = runQuery($mysqli,$sql);
$cols = ['id','last_name','occurrences'];
displayQuery($question,$sql,$cols,$pads);