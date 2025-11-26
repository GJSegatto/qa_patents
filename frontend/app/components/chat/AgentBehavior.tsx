'use client'

import { Button } from "@/components/ui/button"
import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldSet
} from "@/components/ui/field"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Textarea } from "@/components/ui/textarea"
import { Settings } from "lucide-react"
import { useState, useRef } from "react"

export default function AgentBehavior({
    behavior,
    onBehaviorChange
} : { behavior: string; onBehaviorChange: (value: string) => void}) {
    const textareaRef = useRef<HTMLTextAreaElement>(null)

    return (
        <Popover>
            <PopoverTrigger asChild className="items-center">
                <button className="shadow-sm border rounded-xl px-2 cursor-pointer"><Settings className="size-6"/></button>
            </PopoverTrigger>
            <PopoverContent>
                <div className="grid gap-4">
                    <div className="space-y-2">
                        <h4 className="leading-none font-medium">Como o agente deve se comportar?</h4>
                        <p className="text-muted-foreground text-sm  pb-2 border-b">
                        Caso não seja configurado, o agente atuará de forma padrão.
                        </p>
                    </div>

                    <div className="w-full max-w-lg">
                        <FieldSet>
                            <FieldGroup>
                                <Field>
                                    <Textarea
                                        ref={textareaRef}
                                        id="behavior"
                                        defaultValue={behavior? behavior : ""}
                                        placeholder="Como o agente deve se comportar..."
                                        rows={4}
                                    />
                                </Field>
                            </FieldGroup>
                        </FieldSet>
                    </div>

                    <Button
                        className="cursor-pointer"
                        variant={"outline"}
                        onClick={() => onBehaviorChange(textareaRef.current?.value || "")}
                    >
                    Salvar
                    </Button>
                </div>
                

            </PopoverContent>
        </Popover>
    )
}