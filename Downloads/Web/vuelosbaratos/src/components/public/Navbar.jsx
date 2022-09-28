import React from 'react'
import {Link, Route, Routes, BrowserRouter as Router } from 'react-router-dom';



const Navbar = () => {
  return (
    <div id="header">
			<div>
				<Link to={"./"} class="logo"><img src="images/logo.png" alt="" /></Link>
				<ul id="navigation">
					<li class="selected">
						<Link to={"./"}>Inicio</Link>
					</li>
					<li>
						<Link to="./about">Quienes Somos?</Link>
					</li>
					{/* <li class="menu">
						<Link to={"./projects"}>Projects</Link>
						<ul class="primary">
							<li>
								<Link to={"./projects/1"}>proj 1</Link>
							</li>
						</ul>
					</li> */}
				</ul>
			</div>
		</div>
  )
}

export default Navbar
