'use client'

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { FileSearchIcon } from "lucide-react"
import { PropsWithChildren, useState } from "react"

type Role = "user" | "agent";

type SearchPatentProps = PropsWithChildren<{
  role: Role;
}>;

export default function SearchPatent({
    role,
    onSearch
} : SearchPatentProps & { onSearch?: (id:string) => Promise<void> }) {

    const [patentId, setPatentId] = useState("")

    async function search() {
       if (!patentId) return

       if(onSearch) await onSearch(patentId)
    }

    return (
        <Popover>
            <PopoverTrigger asChild className="items-center">
                <button className="shadow-sm border rounded-xl px-2 cursor-pointer"><FileSearchIcon className="size-6"/></button>
            </PopoverTrigger>
            <PopoverContent>
                <div className="grid gap-4">
                    <div className="space-y-2">
                        <h4 className="leading-none font-medium">Pesquisa Avançada por ID</h4>
                        <p className="text-muted-foreground text-sm  pb-2 border-b">
                        Insira abaixo o número de identificação de uma patentes para mais detalhes.
                        </p>
                    </div>

                    <div className="grid gap-2">
                        <div className="flex items-center gap-4">
                            <Label htmlFor="patent_id">ID:</Label>
                            <Input
                                id="patent_id"
                                value={patentId? patentId : ""}
                                onChange={(e) => setPatentId(e.target.value)}
                                defaultValue=""
                                className="col-span-2 h-8"
                            />
                        </div>
                    </div>

                    <Button
                        className="cursor-pointer" 
                        variant={"outline"}
                        onClick={search}
                    >
                    Pesquisar
                    </Button>
                </div>
                

            </PopoverContent>
        </Popover>
    )
}