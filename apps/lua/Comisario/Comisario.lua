-- STEWARD_STUB
-- Comisario ahora se llama Steward (carpeta apps/lua/Steward). Este archivo reemplaza a la app anterior para que
-- no queden dos apps vigilando y sancionando a la vez. No hace nada; esta carpeta se puede borrar.
-- Comisario is now called Steward (apps/lua/Steward). This placeholder does nothing; this folder can be deleted.

function script.windowMain(dt)
  ui.textWrapped('Comisario ahora se llama Steward. Abre la app Steward desde la barra de apps. Esta carpeta (apps/lua/Comisario) ya no se usa y la puedes borrar.')
  ui.textWrapped('Comisario is now called Steward. Open the Steward app from the apps bar. This folder (apps/lua/Comisario) is no longer used and can be deleted.')
end
