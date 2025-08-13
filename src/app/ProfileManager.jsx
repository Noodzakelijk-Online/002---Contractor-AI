import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Trash2, Plus, Settings, Save, Edit } from 'lucide-react'

export function ProfileManager({
  settingsOpen,
  setSettingsOpen,
  profielen,
  bewerkProfiel,
  nieuwProfiel,
  startNieuwProfiel,
  startBewerkProfiel,
  opslaanProfiel,
  verwijderProfiel,
  voegProfielAfdrachtToe,
  updateProfielAfdracht,
  verwijderProfielAfdracht,
  setNieuwProfiel
}) {
  return (
    <Dialog open={settingsOpen} onOpenChange={setSettingsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="h-7 text-xs">
          <Settings className="h-3 w-3 mr-1" />
          Profielen
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[85vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Persoon Profielen Beheren</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Bestaande Profielen */}
          <div>
            <h3 className="text-sm font-medium mb-2">Bestaande Profielen</h3>
            <div className="space-y-2">
              {profielen.map(profiel => (
                <div key={profiel.id} className="flex justify-between items-center p-2 border rounded text-xs">
                  <div>
                    <span className="font-medium">{profiel.naam}</span>
                    <span className="text-muted-foreground ml-2">
                      €{profiel.uurtariefPersoon}/u
                    </span>
                    {profiel.afdrachten.length > 0 && (
                      <span className="text-muted-foreground ml-2">
                        ({profiel.afdrachten.length} afdracht{profiel.afdrachten.length !== 1 ? 'en' : ''})
                      </span>
                    )}
                  </div>
                  <div className="flex gap-1">
                    <Button
                      onClick={() => startBewerkProfiel(profiel)}
                      variant="outline"
                      size="sm"
                      className="h-6 text-xs"
                    >
                      <Edit className="h-3 w-3" />
                    </Button>
                    <Button
                      onClick={() => verwijderProfiel(profiel.id)}
                      variant="destructive"
                      size="sm"
                      className="h-6 text-xs"
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              ))}
              {profielen.length === 0 && (
                <p className="text-xs text-muted-foreground">Nog geen profielen aangemaakt</p>
              )}
            </div>
          </div>

          {/* Profiel Bewerken/Aanmaken */}
          <div className="border-t pt-4">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-sm font-medium">
                {bewerkProfiel ? 'Profiel Bewerken' : 'Nieuw Profiel'}
              </h3>
              {bewerkProfiel && (
                <Button
                  onClick={startNieuwProfiel}
                  variant="outline"
                  size="sm"
                  className="h-6 text-xs"
                >
                  Nieuw
                </Button>
              )}
            </div>

            <div className="grid grid-cols-2 gap-2 mb-3">
              <Input
                className="h-7 text-xs"
                value={nieuwProfiel.naam}
                onChange={(e) => setNieuwProfiel({...nieuwProfiel, naam: e.target.value})}
                placeholder="Naam"
              />
              <Input
                className="h-7 text-xs"
                type="number"
                step="0.01"
                value={nieuwProfiel.uurtariefPersoon}
                onChange={(e) => setNieuwProfiel({...nieuwProfiel, uurtariefPersoon: parseFloat(e.target.value) || 0})}
                placeholder="Persoon €/u"
              />
            </div>

            {/* Afdrachten voor profiel */}
            <div className="mb-3">
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-medium">Mogelijke Afdrachten</label>
                <Button
                  onClick={voegProfielAfdrachtToe}
                  size="sm"
                  variant="outline"
                  className="h-6 text-xs"
                >
                  <Plus className="h-3 w-3 mr-1" />
                  Afdracht
                </Button>
              </div>

              <div className="text-xs text-muted-foreground mb-2">
                <strong>Prioriteit:</strong> Uurloon afdrachten gaan vóór marge afdrachten
              </div>

              {nieuwProfiel.afdrachten.map((afdracht) => (
                <div key={afdracht.id} className="grid grid-cols-5 gap-2 mb-2 p-2 bg-muted/30 rounded">
                  <Select
                    value={afdracht.basis}
                    onValueChange={(value) => updateProfielAfdracht(afdracht.id, 'basis', value)}
                  >
                    <SelectTrigger className="h-6 text-xs">
                      <SelectValue placeholder="Basis" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="uurloon">Uurloon</SelectItem>
                      <SelectItem value="marge">Marge</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select
                    value={afdracht.type}
                    onValueChange={(value) => updateProfielAfdracht(afdracht.id, 'type', value)}
                  >
                    <SelectTrigger className="h-6 text-xs">
                      <SelectValue placeholder="Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="percentage">%</SelectItem>
                      <SelectItem value="vastbedrag">€</SelectItem>
                    </SelectContent>
                  </Select>

                  <Input
                    className="h-6 text-xs"
                    type="number"
                    step={afdracht.type === 'percentage' ? '1' : '0.01'}
                    value={afdracht.waarde}
                    onChange={(e) => updateProfielAfdracht(afdracht.id, 'waarde', parseFloat(e.target.value) || 0)}
                    placeholder={afdracht.type === 'percentage' ? '25' : '50'}
                  />

                  <Select
                    value={afdracht.aanProfielId}
                    onValueChange={(value) => updateProfielAfdracht(afdracht.id, 'aanProfielId', value)}
                  >
                    <SelectTrigger className="h-6 text-xs">
                      <SelectValue placeholder="Aan profiel..." />
                    </SelectTrigger>
                    <SelectContent>
                      {profielen
                        .filter(p => p.id !== bewerkProfiel) // Niet aan jezelf afdragen
                        .map(p => (
                          <SelectItem key={p.id} value={p.id}>
                            {p.naam}
                          </SelectItem>
                        ))}
                    </SelectContent>
                  </Select>

                  <Button
                    onClick={() => verwijderProfielAfdracht(afdracht.id)}
                    size="sm"
                    variant="destructive"
                    className="h-6 text-xs"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              ))}
            </div>

            <Button
              onClick={opslaanProfiel}
              className="w-full h-7 text-xs"
              disabled={!nieuwProfiel.naam.trim()}
            >
              <Save className="h-3 w-3 mr-1" />
              {bewerkProfiel ? 'Wijzigingen Opslaan' : 'Profiel Opslaan'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
