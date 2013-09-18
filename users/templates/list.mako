# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>User's List</h1>

<ul id="tasks">
% if users:
  % for user in users:
  <li>
    <span class="name">${user.name}</span>
    <span class="action">
      ${user.password}
    </span>

  </li>
  % endfor
% else:
  <li>There are no User</li>
% endif
  <li class="last">
    <a href="${request.route_url('new')}">Add a new User</a>
  </li>
  
    <span>
              <a href="${request.application_url}/logout">Logout</a>
    </span>

</ul>