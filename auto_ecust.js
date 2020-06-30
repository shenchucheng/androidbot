function queryDrsj(tjrq='2020-06-30'){
			var flag = false;
			$.ajax({
				type : "POST",
				url : "com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext",
				contentType : "text/json",
				async:false,
				data : wf.jsonString({
					params : {xh:'Y30180448',tjrq:tjrq},
					querySqlId : "com.sudytech.work.uust.zxxsmryb.zxxsmryb.queryDrsj",
				}),
				success : function(data){
					console.log(data)
					var list = data.list;
					if(list && list.length > 0){
						for(var name in list[0]){
							if(list[0][name] && $('div[name='+name.toLowerCase()+']').length==1){
								$('div[name='+name.toLowerCase()+']').sui().setValue(list[0][name]);
							}
						}
						flag = true;
					}
				}
			});
			return flag;
		}
function getinfo(tjrq="2020-06-30", tjsj="2020-06-30 21:08"){
			if(!$('.sui-form').sui().validate()){
				alert("请检查输入项！");
				return;
			}
			var entity=$('.sui-form').sui().getValue();
            entity.swdqtw = "36.6";
			entity.tjrq=tjrq;
            tjsj=tjsj.startsWith(tjrq)?tjsj:[tjrq, tjsj].join(' ');
            entity.tjsj=tjsj;
            entity.ss=entity.xq+"-"+entity.ss+"-"+entity.mph;
			entity.tUustMrybhdgjs = JSON.parse(entity.tUustMrybhdgjs);
            for (var i=0, lis=entity.tUustMrybhdgjs, l=lis.length; i<l; i++){
                var  wcrq=lis[i]['wcrq'];
                lis[i]['wcrq']=wcrq==tjrq?wcrq:tjrq
            }
			entity.__type="sdo:com.sudytech.work.uust.zxxsmryb.zxxsmryb.TUustZxxsmryb";
			if(entity.tjsj=="" || entity.tjsj==null){
				location.reload();//页面刷新
				return;
			}
			if(entity.id=="" || entity.id==null || flag==false){
				delete entity.id;
			}
			return entity
		}

function saveOrUpdate1(tjrq="2020-06-30", tjsj="2020-06-30 21:08"){
			if(!$('.sui-form').sui().validate()){
				alert("请检查输入项！");
				return;
			}
			var entity=$('.sui-form').sui().getValue();
            entity.swdqtw = "36.6";
			entity.tjrq=tjrq;
            tjsj=tjsj.startsWith(tjrq)?tjsj:[tjrq, tjsj].join(' ');
            entity.tjsj=tjsj;
            entity.ss=entity.xq+"-"+entity.ss+"-"+entity.mph;
			entity.tUustMrybhdgjs = JSON.parse(entity.tUustMrybhdgjs);
            for (var i=0, lis=entity.tUustMrybhdgjs, l=lis.length; i<l; i++){
                var  wcrq=lis[i]['wcrq'];
                lis[i]['wcrq']=wcrq==tjrq?wcrq:tjrq
            }
			entity.__type="sdo:com.sudytech.work.uust.zxxsmryb.zxxsmryb.TUustZxxsmryb";
			if(entity.tjsj=="" || entity.tjsj==null){
				location.reload();//页面刷新
				return;
			}
			if(entity.id=="" || entity.id==null || flag==false){
				delete entity.id;
			}
			return entity
		}
# 注意entity.ID
