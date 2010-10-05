var w = document.body.clientWidth,
    h = document.body.clientHeight - 60,
    colors = pv.Colors.category19();

var vis = new pv.Panel()
    .width(w)
    .height(h)
    .fillStyle("white")
    .event("mousedown", pv.Behavior.pan())
    .event("mousewheel", pv.Behavior.zoom());

var force = vis.add(pv.Layout.Force)
	.def("cc", -200)
    .nodes(conf_data.nodes)
    .links(conf_data.links)
	.springLength(300)
	.springConstant(0.25) // attractive force
	.springDamping(0.1) 
	.chargeMinDistance(80)
	.chargeConstant(function(){return this.cc()})
	//.chargeConstant(-20)
	.bound(true)

	;

force.link.add(pv.Line);

force.node.add(pv.Dot)
    .size(function(d){return (d.linkDegree + 40) * Math.pow(this.scale, -1.5)})
    .fillStyle(function(d){ return d.fix ? "brown" : colors(d.group)})
    .strokeStyle(function(){ return this.fillStyle().darker()})
    .lineWidth(1)
    .title(function(d){ return d.nodeName})
    .event("mousedown", pv.Behavior.drag())
    .event("drag", force)
	.add(pv.Image)
		.url(function(d){return d.img_url})
		.width(function(d){return 12+ d.linkDegree*1.4;} )
		.height(function(d){return 12 + d.linkDegree*1.4});

vis.render();
