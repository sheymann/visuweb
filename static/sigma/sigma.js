var sigmaDOM;

function setSiGMa(){ if(!sigmaDOM){ sigmaDOM = (navigator.appName.indexOf("Microsoft")!=-1) ? window["SiGMa-DOM"] : document["SiGMa-DOM"]; } return sigmaDOM;}

// Graph generation:
function getRandomGraph(){
	// Here are the dimensions of the graph:
	var N = 100, M = 250;
	var minSize = 1, maxSize = 100;
	var i, from, to;
	
	var graph = {'nodes': [], 'edges': []};
	var linked = {};
	
	// Add nodes:
	for(i=0;i<N;i++){
		graph['nodes'].push({
			'id': 'node_'+i,
			'label': 'Node '+i,
			'size': (maxSize-minSize)*Math.random()+minSize
		});
	}
	
	// Add edges
	for(i=0;i<M;i++){
		from = Math.floor(N*Math.random());
		to = Math.floor((N-1)*Math.random());
		
		// To be sure the extremities are not the same:
		to = (to==from) ? to+1 : to;
		
		graph['edges'].push({
			'id': 'edge_'+i,
			'sourceID': 'node_'+from,
			'targetID': 'node_'+to
		});
		
		linked['node_'+from] = 1;
		linked['node_'+to] = 1;
	}
	
	// Remove orphans
	graph['nodes'] = graph['nodes'].filter(function(e){return linked[e.id]==1});
	
	return graph;
}

// On SiGMa ready callback:
function feedSiGMa(){
	if(!setSiGMa()){ return;}
	
	sigmaDOM.resetGraphPosition();
	sigmaDOM.killForceAtlas();
	sigmaDOM.deleteGraph();
	sigmaDOM.updateGraph(getRandomGraph());
	sigmaDOM.initForceAtlas();
}

// Callbacks:
function onClickNodes(){
	//var url = ;
	//window.open(url);
}

function onOverNodes(){

}

// Initialization:
window.onload = function(){ setSiGMa(); }

//Functions (switches)

function switchFishEye(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.isFishEye()){sigmaDOM.deactivateFishEye();}else{sigmaDOM.activateFishEye();}
}

var isLayouting = true;
function switchLayouting(){
	if(!setSiGMa()){ return;}
	if(isLayouting){sigmaDOM.killForceAtlas(); isLayouting=false;}else{sigmaDOM.initForceAtlas(); isLayouting=true;}
}

function switchDisplayEdges(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getDisplayEdges()){sigmaDOM.setDisplayEdges(false);}else{sigmaDOM.setDisplayEdges(true);}
}

function switchDisplayNodes(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getDisplayNodes()){sigmaDOM.setDisplayNodes(false);}else{sigmaDOM.setDisplayNodes(true);}
}

function switchDisplayLabels(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getDisplayLabels()){sigmaDOM.setDisplayLabels(false);}else{sigmaDOM.setDisplayLabels(true);}
}

function switchUseEdgeSizes(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getUseEdgeSizes()){sigmaDOM.setUseEdgeSizes(false);}else{sigmaDOM.setUseEdgeSizes(true);}
}

function switchDraggable(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getDraggable()){sigmaDOM.setDraggable(false);}else{sigmaDOM.setDraggable(true);}
}

function switchZoomable(){
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getZoomable()){sigmaDOM.setZoomable(false);}else{sigmaDOM.setZoomable(true);}
}

//Functions (other)

function rotateGraph(){
	if(!setSiGMa()){ return;}
	sigmaDOM.rotate(document.getElementById('rotateAngle').value,0,0);
}

function changeMinDisplaySize(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setMinDisplaySize(document.getElementById('minDisplaySize').value);
}

function displayMinDisplaySize(){
	if(!setSiGMa()){ return;}
	document.getElementById('minDisplaySize').value = sigmaDOM.getMinDisplaySize();
}

function changeMaxDisplaySize(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setMaxDisplaySize(document.getElementById('maxDisplaySize').value);
}

function displayMaxDisplaySize(){
	if(!setSiGMa()){ return;}
	document.getElementById('maxDisplaySize').value = sigmaDOM.getMaxDisplaySize();
}

function changeMinDisplayThickness(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setMinDisplayThickness(document.getElementById('minDisplayThickness').value);
}

function displayMinDisplayThickness(){
	if(!setSiGMa()){ return;}
	document.getElementById('minDisplayThickness').value = sigmaDOM.getMinDisplayThickness();
}

function changeMaxDisplayThickness(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setMaxDisplayThickness(document.getElementById('maxDisplayThickness').value);
}

function displayMaxDisplayThickness(){
	if(!setSiGMa()){ return;}
	document.getElementById('maxDisplayThickness').value = sigmaDOM.getMaxDisplayThickness();
}

function changeTextThreshold(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setTextThreshold(document.getElementById('textThreshold').value);
}

function displayTextThreshold(){
	if(!setSiGMa()){ return;}
	document.getElementById('textThreshold').value = sigmaDOM.getTextThreshold();
}

function changeGraphCenterX(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setCenterX(document.getElementById('graphCenterX').value);
}

function displayGraphCenterX(){
	if(!setSiGMa()){ return;}
	document.getElementById('graphCenterX').value = sigmaDOM.getCenterX();
}
	
function changeGraphCenterY(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setCenterY(document.getElementById('graphCenterY').value);
}

function displayGraphCenterY(){
	if(!setSiGMa()){ return;}
	document.getElementById('graphCenterY').value = sigmaDOM.getCenterY();
}
	
function changeGraphZoomRatio(){
	if(!setSiGMa()){ return;}
	sigmaDOM.setZoomRatio(document.getElementById('graphZoomRatio').value);
}

function displayGraphZoomRatio(){
	if(!setSiGMa()){ return;}
	document.getElementById('graphZoomRatio').value = sigmaDOM.getZoomRatio();
}

function displayDefaultEdgeType(){
	if(!setSiGMa()){ return;}
	switch (sigmaDOM.getDefaultEdgeType()){
	case  0: document.getElementById('defaultEdgeTypeRadio0').checked = true; break;
	case  1: document.getElementById('defaultEdgeTypeRadio1').checked = true; break;
	case  2: document.getElementById('defaultEdgeTypeRadio2').checked = true; break;
	case  3: document.getElementById('defaultEdgeTypeRadio3').checked = true; break;
	default: document.getElementById('defaultEdgeTypeRadio0').checked = true; break;
	}
}

function switcher(){
	var on = "twitter.jpg";
	var off = "facebook.jpg";
	var src = document.getElementById('switcher_img').src;
	if(!setSiGMa()){ return;}
	if(sigmaDOM.getDisplayEdges()){sigmaDOM.setDisplayEdges(false);document.getElementById('switcher_img').src=off;}
		else{sigmaDOM.setDisplayEdges(true);document.getElementById('switcher_img').src=on;}
}

function init(){
	displayMinDisplaySize(); 
	displayMaxDisplaySize(); 
	displayMinDisplayThickness(); 
	displayMaxDisplayThickness(); 
	displayDefaultEdgeType();
	displayTextThreshold();
	displayGraphCenterX();
	displayGraphCenterY();
	displayGraphZoomRatio();
}
