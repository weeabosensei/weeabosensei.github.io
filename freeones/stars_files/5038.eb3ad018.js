(self.webpackChunk=self.webpackChunk||[]).push([[5038],{54929:function(e,t,l){var i={"./de.json":79377,"./en.json":55621,"./es.json":38822,"./fr.json":19111,"./it.json":31895,"./nl.json":92456,"./pt.json":8825};function o(e){var t=s(e);return l(t)}function s(e){if(!l.o(i,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return i[e]}o.keys=function(){return Object.keys(i)},o.resolve=s,e.exports=o,o.id=54929},25038:function(e,t,l){"use strict";l.d(t,{Z:function(){return n}});l(2503);var i=l(32698),o=l(9733),s=l(13171),a=l(58338);const r=new o.Z;function n(e,t="show-collection-modal-"){const l=(0,a.oR)(),o=e;return{CollectionModal:i.Z,show:()=>{l.state.user?s.Z.emit(t+o):r.register()},uniqueModalId:o}}},18381:function(e,t,l){"use strict";l.d(t,{Z:function(){return s}});var i=l(52861),o=l(55959);function s(){const e=(0,o.ref)(""),t=(0,o.ref)(""),l=(0,o.ref)("private"),s=(0,o.ref)(""),a=(0,o.ref)(!1),r=(0,o.ref)("video"),n=(0,o.ref)(""),c=(0,o.getCurrentInstance)();return{description:e,name:t,visibility:l,email:s,status:n,contentType:r,loading:a,createCollectionPost:(e,t,l)=>{i.Z.post("/my/collection/add",{name:e,description:t,visibility:l,status:n.value,contentType:r.value}).then((i=>{c.emit("close",i.data),a.value=!1,e.value="",t.value="",n.value="",l.value="private"})).catch((()=>{a.value=!1}))}}}},32698:function(e,t,l){"use strict";l.d(t,{Z:function(){return C}});var i=l(55959),o=l(13171),s=l(95419),a=l(52861),r=l(67948),n=l(80928),c=l(18381);const u={key:0},d={key:1},p={key:0},y={key:0},v={class:"form-group mb-0"},m={class:"font-bold"},f={class:"flex flex-row mb-2"},P={class:"select-wrapper flex items-center w-2/3 mr-2"},b=["value"],g=["onClick"];var C={__name:"CollectionModal",props:{contentType:{type:String,default:""},typeId:{type:String,default:""},isFollowingMutation:{type:Boolean,default:!1}},setup(e){const t=e,{t:C}=(0,n.T_)(l(54929)),{loading:h,createCollectionPost:N}=(0,c.Z)(),k=(0,i.defineAsyncComponent)({loader:()=>l.e(4874).then(l.bind(l,24874)),loadingComponent:s.Z}),w=(0,i.getCurrentInstance)(),T=(0,i.inject)("uniqueModalId"),S=(0,i.ref)(!1),E=(0,i.ref)(void 0),A=(0,i.ref)(!1),F=(0,i.ref)(!1),Z=(0,i.ref)(!1),j=(0,i.ref)(null),V=()=>{let e;h.value=!0,"video"===t.contentType&&(e={collectionId:j.value.value}),a.Z.post(`/user-favorite/${t.contentType}/${t.typeId}/add`,e).then((e=>{h.value=!1,Z.value=!0,E.value=!0,w.appContext.config.globalProperties.$modal.show(T),o.Z.emit("contentAddedToCollection",{contentType:t.contentType,typeId:t.typeId})})).catch((e=>{r.Z.error(e.message,e)}))},x=e=>{e&&(S.value.unshift(e),j.value.value=e.id),F.value=!F.value};return o.Z.on("show-collection-modal-"+T,(()=>{if(w.appContext.config.globalProperties.$modal.show(T),Z.value=t.isFollowingMutation,"video"!==t.contentType||Z.value){if(Z.value)return h.value=!0,E.value=!1,void a.Z.post(`/user-favorite/${t.contentType}/${t.typeId}/remove`).then((e=>{h.value=!1,Z.value=!1,o.Z.emit("contentRemovedFromCollection",{contentType:t.contentType,typeId:t.typeId})})).catch((e=>{r.Z.error(e.message,e)}));V()}else A.value||a.Z.post("/my/collections/get",{contentType:t.contentType}).then((e=>{S.value=e.data,h.value=!1,A.value=!0})).then((e=>{0===S.value.length&&N(C("myFirstPlaylist"),"","private")})).catch((e=>{h.value=!1,r.Z.error(e.response)}))})),o.Z.on("global-modal-hide"+T,(()=>{F.value=!1,E.value=void 0})),(t,l)=>{const o=(0,i.resolveComponent)("Modal");return(0,i.openBlock)(),(0,i.createBlock)(o,null,{title:(0,i.withCtx)((()=>["video"===e.contentType&&void 0===E.value?((0,i.openBlock)(),(0,i.createElementBlock)("div",u,(0,i.toDisplayString)((0,i.unref)(C)("addToCollection")),1)):((0,i.openBlock)(),(0,i.createElementBlock)("div",d,(0,i.toDisplayString)((0,i.unref)(C)(E.value?"successfullyAdded":"successfullyRemoved")),1))])),body:(0,i.withCtx)((()=>[(0,i.unref)(h)?(0,i.createCommentVNode)("v-if",!0):((0,i.openBlock)(),(0,i.createElementBlock)("div",p,["video"===e.contentType&&void 0===E.value?((0,i.openBlock)(),(0,i.createElementBlock)("div",y,[(0,i.createElementVNode)("form",null,[(0,i.withDirectives)((0,i.createElementVNode)("div",v,[(0,i.createElementVNode)("label",m,(0,i.toDisplayString)((0,i.unref)(C)("yourPlaylists")),1),(0,i.createElementVNode)("div",f,[(0,i.createElementVNode)("div",P,[(0,i.createElementVNode)("select",{id:"collections",ref_key:"collectionId",ref:j,class:"form-control border-none"},[((0,i.openBlock)(!0),(0,i.createElementBlock)(i.Fragment,null,(0,i.renderList)(S.value,(e=>((0,i.openBlock)(),(0,i.createElementBlock)("option",{key:e.id,value:e.id},(0,i.toDisplayString)(e.name),9,b)))),128))],512)]),(0,i.createElementVNode)("button",{type:"button",class:"btn btn-primary flex-1",onClick:(0,i.withModifiers)(V,["prevent"])},(0,i.toDisplayString)((0,i.unref)(C)("addToCollection")),9,g)]),(0,i.createElementVNode)("a",{href:"#",class:"font-size-s hand",onClick:l[0]||(l[0]=e=>x())},(0,i.toDisplayString)((0,i.unref)(C)("createNewPlaylist")),1)],512),[[i.vShow,!F.value]]),F.value?((0,i.openBlock)(),(0,i.createBlock)((0,i.unref)(k),{key:0,onClose:x})):(0,i.createCommentVNode)("v-if",!0)])])):(0,i.createCommentVNode)("v-if",!0)]))])),_:1})}}}},79377:function(e){"use strict";e.exports=JSON.parse('{"createPlaylist":"Wiedergabeliste speichern","addToCollection":"Ergänzen","removeFromCollection":"Entfernen von","successfullyAdded":"Erfolgreich hinzugefügt","successfullyRemoved":"Erfolgreich entfernt","yourPlaylists":"Ihre Wiedergabelisten","createNewPlaylist":"Neuen wiedergabeliste erstellen","namePlaylist":"Name Wiedergabeliste","visibility":"Sichtweite","private":"Privat","public":"Öffentlichkeit","description":"Beschreibung","myFirstPlaylist":"Meine erste Wiedergabeliste"}')},55621:function(e){"use strict";e.exports=JSON.parse('{"createPlaylist":"Save Playlist","addToCollection":"Add to","removeFromCollection":"Remove from","successfullyAdded":"Successfully Added","successfullyRemoved":"Successfully Removed","yourPlaylists":"Your Playlists","createNewPlaylist":"Create new playlist","namePlaylist":"Name Playlist","visibility":"Visibility","private":"Private","public":"Public","description":"Description","myFirstPlaylist":"My first playlist"}')},38822:function(e){"use strict";e.exports=JSON.parse('{"createPlaylist":"Guardar lista de reproducción","addToCollection":"Añadir","removeFromCollection":"Eliminar de","successfullyAdded":"Agregado exitosamente","successfullyRemoved":"Eliminado con éxito","yourPlaylists":"Tus listas de reproducción","createNewPlaylist":"Crear nueva lista de reproducción","namePlaylist":"Lista de reproducción de nombre","private":"Privado","public":"Público","visibility":"Visibilidad","description":"Descripción","myFirstPlaylist":"Mi primera lista de reproducción"}')},19111:function(e){"use strict";e.exports=JSON.parse('{"createPlaylist":"Enregistrer la playlist","addToCollection":"Ajouter à","removeFromCollection":"Retirer","successfullyAdded":"ajouté avec succès","successfullyRemoved":"Supprimé avec succès","yourPlaylists":"Vos listes de lecture","createNewPlaylist":"Créer une nouvelle playlist","namePlaylist":"Nom de la liste de lecture","visibility":"Visibilité","description":"La description","private":"Privé","public":"Publique","myFirstPlaylist":"Ma première playlist"}')},31895:function(e){"use strict";e.exports=JSON.parse('{"addToCollection":"Aggiungere a","removeFromCollection":"Rimuovere da","successfullyAdded":"Aggiunto con successo","successfullyRemoved":"Rimosso con successo","yourPlaylists":"Le tue playlist","createNewPlaylist":"Crea nuova playlist","namePlaylist":"Nome playlist","visibility":"Visibilità","description":"Descrizione","private":"Privato","public":"Pubblico","createPlaylist":"Salva playlist","myFirstPlaylist":"La mia prima playlist"}')},92456:function(e){"use strict";e.exports=JSON.parse('{"addToCollection":"Voeg toe aan","removeFromCollection":"Verwijderen uit","successfullyAdded":"succesvol toegevoegd","successfullyRemoved":"Succesvol verwijderd","yourPlaylists":"Je afspeellijsten","createNewPlaylist":"Maak nieuwe afspeellijst","namePlaylist":"Naam afspeellijst","visibility":"Zichtbaarheid","description":"Omschrijving","private":"Prive","public":"Openbaar","createPlaylist":"Afspeellijst opslaan","myFirstPlaylist":"Mijn eerste playlist"}')},8825:function(e){"use strict";e.exports=JSON.parse('{"addToCollection":"Adicionar à","removeFromCollection":"Remover de","successfullyAdded":"Adicionado com sucesso","successfullyRemoved":"Removido com Sucesso","yourPlaylists":"Suas listas de reprodução","createNewPlaylist":"Crie uma nova lista de reprodução","namePlaylist":"Nome da lista de reprodução","createPlaylist":"Salvar lista de reprodução","visibility":"Visibilidade","description":"Descrição","private":"Privado","public":"Público","myFirstPlaylist":"Minha primeira playlist"}')}}]);