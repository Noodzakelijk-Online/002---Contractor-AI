import { Button } from '@/components/ui/button.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Users, Calculator } from 'lucide-react'
import './App.css'
import { ProfileManager } from './app/ProfileManager'
import { Summary } from './app/Summary'
import { PersonRow } from './app/PersonRow'
import { useUrenregistratie } from './hooks/useUrenregistratie'

function App() {
  const {
    personen,
    profielen,
    settingsOpen,
    setSettingsOpen,
    bewerkProfiel,
    nieuwProfiel,
    setNieuwProfiel,
    voegPersoonToe,
    verwijderPersoon,
    updateTijdregistratie,
    updateKlanttarief,
    updateActieveAfdrachten,
    startNieuwProfiel,
    startBewerkProfiel,
    opslaanProfiel,
    verwijderProfiel,
    voegProfielAfdrachtToe,
    updateProfielAfdracht,
    verwijderProfielAfdracht,
    berekenFinancieel,
    totalen,
    uitbetalingen,
  } = useUrenregistratie()

  return (
    <div className="min-h-screen bg-background p-2">
      <div className="max-w-6xl mx-auto">
        {/* Compacte Header met Settings */}
        <div className="mb-3 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold flex items-center gap-2">
              <Calculator className="h-5 w-5" />
              Urenregistratie Calculator
            </h1>
          </div>

          <ProfileManager
            settingsOpen={settingsOpen}
            setSettingsOpen={setSettingsOpen}
            profielen={profielen}
            bewerkProfiel={bewerkProfiel}
            nieuwProfiel={nieuwProfiel}
            startNieuwProfiel={startNieuwProfiel}
            startBewerkProfiel={startBewerkProfiel}
            opslaanProfiel={opslaanProfiel}
            verwijderProfiel={verwijderProfiel}
            voegProfielAfdrachtToe={voegProfielAfdrachtToe}
            updateProfielAfdracht={updateProfielAfdracht}
            verwijderProfielAfdracht={verwijderProfielAfdracht}
            setNieuwProfiel={setNieuwProfiel}
          />
        </div>

        <Summary totalen={totalen} uitbetalingen={uitbetalingen} />

        {/* Personen Sectie */}
        <Card className="p-2">
          <CardHeader className="p-0 mb-2">
            <div className="flex justify-between items-center">
              <CardTitle className="text-sm">Personen & Uren</CardTitle>
              <div className="flex gap-2">
                {profielen.length > 0 ? (
                  <Select onValueChange={(profielId) => voegPersoonToe(profielId)}>
                    <SelectTrigger className="h-7 w-32 text-xs">
                      <SelectValue placeholder="Voeg persoon toe..." />
                    </SelectTrigger>
                    <SelectContent>
                      {profielen.map(profiel => (
                        <SelectItem key={profiel.id} value={profiel.id}>
                          {profiel.naam}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : (
                  <div className="text-xs text-muted-foreground">Maak eerst profielen aan</div>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {personen.length === 0 ? (
              <div className="text-center py-4 text-muted-foreground">
                <Users className="h-6 w-6 mx-auto mb-2 opacity-50" />
                <p className="text-xs">Selecteer een profiel om te beginnen</p>
              </div>
            ) : (
              <div className="space-y-2">
                {personen.map((persoon) => (
                  <PersonRow
                    key={persoon.id}
                    persoon={persoon}
                    profiel={profielen.find(p => p.id === persoon.profielId)}
                    berekenFinancieel={berekenFinancieel}
                    updateTijdregistratie={updateTijdregistratie}
                    updateKlanttarief={updateKlanttarief}
                    verwijderPersoon={verwijderPersoon}
                    updateActieveAfdrachten={updateActieveAfdrachten}
                    profielen={profielen}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App
