%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<title>SDN DETECTIVE</title>
	
	<link rel="stylesheet" href="main.css" />
</head>
 
<body id="index" class="home">
 
	<header id="banner" class="body">
	        <h1><img src="security_guard_icon_mod.png" alt="Logo" class="photo" />
                <a href="/">SDN DETECTIVE <strong>IDS system using RYU controller</strong></a></h1> 
		<nav><ul>
			<li ><a href="/">Home</a></li>
			<li ><a href="/packets">Traffic</a></li>
	 
			<li><a href="/attacks">Attacks</a></li>
                        <li><a href="/action">Action</a></li>
			<li class="active"><a href="/rules">Rules</a></li>
		</ul></nav>
	 
	</header><!-- /#banner -->	
	
	<section id="content" class="body">
		<header>
			<h2 class="entry-title">The IDS rules to catch attacks</h2>
		</header>
		<section>
			<article>
				<div class="entry-content">
                                     <div class="ruleBox">  
					%for row in rows:
						<p>{{row}}</p>
					%end
                                     </div>
				</div><!-- /.entry-content -->
			</article>
		</section>
		<footer class="post-info">
                     <form action="http://localhost:8080/editRules" method="get">
                           <button class ="button editButton">Edit Rules</button>

                     </form>
		</footer>
	 
				
	</section><!-- /#content --> 
</body>
</html>
